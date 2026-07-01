import hashlib
import pandas
from typing import List
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urljoin, urlparse
from typing import List, Dict, Union
import re


def hash_url(url: str) -> str:
    hash_object = hashlib.md5(url.encode())
    return hash_object.hexdigest()


def get_erroronous_url_id(parquet_path: str) -> List[str]:
    df = pd.read_parquet(parquet_path)
    df = df[df['status'] != 200]
    res = df['url_id'].tolist()
    print(f"{parquet_path} analysis finished, {len(res)} problematic URLs")
    return res

def clean_data(html: str) -> str:
    first_stage_cleaned = bytes(re.sub(u'\u0001', '', html)
                                .replace("\n", " ")
                                .replace("\r", " ")
                                .replace("\r\n", " "), 'utf-8')\
        .decode('utf-8', 'ignore')
    final_stage_cleaned = ''.join(
        x for x in first_stage_cleaned if x.isprintable())
    return final_stage_cleaned


def get_hrefs(html: str, url: str, url_id: str) -> Dict[str, Union[str, List[Dict[str, str]]]]:
    def join_url(url: str, href: str) -> str:
        try:
            result = urljoin(url, href)
        except:
            result = href
        return result
    def get_type_of_link(s_link: str, url: str) -> str:
        if "tel:" in s_link.lower():
            d_link = {"page_type": "telephone",
                      "url": s_link, "url_id": hash_url(s_link)}
        elif len(s_link) > 1 and "#" in s_link:
            d_link = {"page_type": "anchor",
                      "url": join_url(url, s_link), "url_id": hash_url(join_url(url, s_link))}
        elif "mailto:" in s_link:
            d_link = {"page_type": "email", "url": s_link,
                      "url_id": hash_url(s_link)}
        elif "javascript:" in s_link:
            d_link = {"page_type": "javascript",
                      "url": s_link, "url_id": hash_url(s_link)}
        else:
            d_link = {"page_type": "http link",
                      "url": join_url(url, s_link), "url_id": hash_url(join_url(url, s_link))}
        return d_link
    soup = BeautifulSoup(html, "lxml")
    links = [elem.get("href") for elem in soup.find_all("a", href=True)]
    extractions = [get_type_of_link(elem, url) for elem in links]
    extractions_wo_self_links = [
        elem for elem in extractions if elem['url'] != url]
    print(f"{url_id} has {len(extractions)} subpages")
    return {"url_id": url_id, "subpages": extractions_wo_self_links}

def generate_href_edge(links_data: Dict[str, Union[str, List[Dict[str, str]]]]) -> List[Dict[str, str]]:
    subpages = links_data["subpages"]
    return [{"source": links_data["url_id"], "target": elem["url_id"]} for elem in subpages]
