import pandas as pd
import os
import subprocess

#os.environ['ARROW_LIBHDFS_DIR'] = '/opt/cloudera/parcels/CDH/lib64/'
#
#for i in range(38):
#
#    df = pd.read_csv(f"hdfs:///user/dyao/html_contents_clean_extra/crawled_html_chunk_{2670+i}.csv",
#                     sep=u"\u0001", header=None, encoding="utf-8", names=["url_id", "status", "html", "partition_id"])
#
#    df['partition_id'] = df['url_id'].apply(lambda x: x[0:2])
#
#    df.to_csv(f"hdfs:///user/dyao/html_contents_clean/crawled_html_chunk_{2670+i}.csv",
#              header=False, sep=u'\u0001', index=False, encoding="utf-8")
#    print(f"crawled_html_chunk_{2670+i}.csv finished")

for i in range(60):
    a = subprocess.call(
        [f"hadoop fs -cp /user/dyao/html_contents_clean_extra/crawled_html_chunk_{2610+i}.csv /user/dyao/html_contents_clean/crawled_html_chunk_{2610+i}.csv"], shell=True)
    b = "success" if a == 0 else "fail"
    print(f"crawled_html_chunk_{2670+i}.csv {b}")
