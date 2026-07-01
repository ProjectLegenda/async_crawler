import pandas as pd
from utils import hash_url
from urllib.request import urlparse

t_proto_url = pd.read_csv("/home/cdsw/input/url_list.csv")

raw_urls = t_proto_url['URL'].tolist()

url_list = list(set([urlparse(elem, "http").geturl().replace("///", "//") for elem in raw_urls]))

url_id = [hash_url(url) for url in url_list]
levels = ["level_0"] * len(url_list)

t_url = pd.DataFrame({'url_id': url_id, 'url': url_list, 'level': levels})

t_url.to_parquet("/home/cdsw/output/crawled_outputs/T_URL.parquet", index=False)
