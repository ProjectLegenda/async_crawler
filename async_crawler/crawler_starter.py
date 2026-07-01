from crawler import crawl_all
import pandas as pd
from datetime import datetime
import asyncio
import sys
import time
import argparse
from async_logger import AsyncLogger
import os
from utils import clean_data

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="input configuration of crawler")
    parser.add_argument("--url_path", type=str,
                        help="specify path of url list required to be crawled", required=True)
    parser.add_argument("--url_chunk_num", type=int,
                        help="specify the chunk number of crawled url list", required=True)
    parser.add_argument("--file_chunk_num", type=int,
                        help="specify the chunk number of crawled html data", required=True)
    os.environ['ARROW_LIBHDFS_DIR'] = '/opt/cloudera/parcels/CDH/lib64/'
    args = parser.parse_args()
    url_path = str(args.url_path)
    chunk_num = int(args.url_chunk_num)
    file_chunk_num = int(args.file_chunk_num)
    name = f"crawled_html_chunk_{file_chunk_num}"
    loop = asyncio.get_event_loop()
    logger = AsyncLogger(name=name, loop=loop).get_logger()
    df = pd.read_csv(url_path)
    urls = df[['url_id', 'url']].to_dict('index')
    url_list = [urls[key] for key in urls.keys()]
    results = loop.run_until_complete(crawl_all(url_list[(10000 * chunk_num - 10000):(10000 * chunk_num)], 300.0, logger))

    cleaned_results = [{'url_id': elem['url_id'], 'status': elem['status'], 'html': clean_data(elem['html']), 'destination_url': elem['destination_url']} for elem in results]
    cleaned_results2 = [{'url_id': elem['url_id'], 'status': elem['status']} for elem in results]
#    loop.close()
    crawled_html = pd.DataFrame(cleaned_results2)
    
    crawled_html.to_csv('crawed_html.csv',index=False)

    for item in cleaned_results:
        with open(item['url_id'],'w') as f:
            print(item['html'],file=f)


               
