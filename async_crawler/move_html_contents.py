import subprocess

root = "hdfs:///user/dyao/"

file_names = [f'crawled_html_chunk_{i + 1}.parquet' for i in range(1718)]

for file_name in file_names:
	subprocess.call([f'hadoop fs -mv {root}{file_name} {root}html_contents/{file_name}'], shell=True)
	print(f'{file_name} finished')

