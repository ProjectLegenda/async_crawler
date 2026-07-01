import pandas as pd
import os
from pandas import DataFrame
from yarl import URL

os.environ['ARROW_LIBHDFS_DIR'] = '/opt/cloudera/parcels/CDH/lib64/'

def get_destination_urls(dataset_name: str) -> DataFrame:
    df = pd.read_csv(f"hdfs:///user/dyao/html_contents_w_dest_url/{dataset_name}", header=None,
                     sep=u"\u0001", encoding="utf-8", names=["url_id", "status", "html", "destination_url"])
    df = df[df['status'] > 0]
    return df[['url_id', 'destination_url']]

def replace_scheme(url: str) -> str:
    return URL(url).with_scheme("https").human_repr()

def add_www_header(url: str) -> str:
    host = URL(url).host
    if host[0:4] != 'www.':
        r_host = 'www.' + host
    else:
        r_host = host
    return URL(url).with_host(r_host).human_repr()

def compare_original_destination_url(original_url: str, destination_url: str) -> int:
    original = add_www_header(replace_scheme(original_url))
    destination = add_www_header(replace_scheme(destination_url))
    if original == destination:
        flag = 0
    elif URL(original).host == URL(destination).host:
        flag = 1
    else:
        flag = 2
    return flag


df = pd.concat([get_destination_urls(f"crawled_html_chunk_{i+1}.csv") for i in range(14)], ignore_index=True, sort=False)
t_url = pd.read_parquet("hdfs:///user/dyao/T_URL.parquet")
final_df = t_url.merge(df, on=['url_id'], how='inner')
final_df = final_df[['url_id', 'url', 'destination_url']]
final_df['redirect_flag'] = final_df.apply(lambda row: compare_original_destination_url(row['url'], row['destination_url']), axis=1)
final_df.to_parquet("hdfs:///user/dyao/T_URL_depth0_w_redirect_flag.parquet", index=False)
#final_df['url'] = final_df['url'].apply(lambda x: add_www_header(replace_scheme(x)))
#final_df['destination_url'] = final_df['destination_url'].apply(lambda x: add_www_header(replace_scheme(x)))
#test = final_df[final_df.apply(lambda row: URL(row['url']).host != URL(row['destination_url']).host, axis=1)]
#print(len(test))
#test = final_df[final_df.apply(lambda row: row['url'] != row['destination_url'], axis=1)]
#print(len(test))
#print(len(final_df))
