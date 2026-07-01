import pandas as pd
import os
from utils import clean_data

os.environ['ARROW_LIBHDFS_DIR'] = '/opt/cloudera/parcels/CDH/lib64/'

file_chunks = [i + 2609 for i in range(61)]

crawled_list = [2624, 2635, 2637, 2642, 2649, 2651, 2665]

file_chunks_unprocessed = [elem for elem in file_chunks if elem not in crawled_list]


for chunk in file_chunks_unprocessed:
    df = pd.read_parquet(
        f"hdfs:///user/dyao/html_contents/crawled_html_chunk_{chunk}.parquet")

    print(max(df['html'].apply(lambda x: len(x)).tolist()))

    df['html'] = df['html'].apply(lambda x: clean_data(x))

    df['partition_id'] = df['url_id'].apply(lambda x: x[0:2])

    df.to_csv(f"hdfs:///user/dyao/html_contents_clean_extra/crawled_html_chunk_{chunk}.csv",
              sep=u'\u0001', index=False, header=False, encoding='utf-8')
    print(f"crawled_html_chunk_{chunk} finished")
