from utils import get_erroronous_url_id
import itertools
import pandas as pd
import os

root = "hdfs:///user/dyao/html_contents/"

os.environ['ARROW_LIBHDFS_DIR'] = '/opt/cloudera/parcels/CDH/lib64/'

files = [f"crawled_html_chunk_{i+1721}.parquet" for i in range(520)]

error_urls = [get_erroronous_url_id(f"{root}{elem}") for elem in files]
error_urls = pd.DataFrame({'url_id': list(itertools.chain.from_iterable(error_urls))})
urls = pd.read_parquet(f"hdfs:///user/dyao/T_URL_depth2.parquet")
error_url = urls.merge(error_urls, how="inner", on="url_id")
error_url.to_parquet(f"{root}trial_iteration_2.parquet", index=False)
print(len(error_urls))
