from os import listdir
from os.path import isfile, join
import subprocess

file_path = "/home/cdsw/output/crawled_outputs"

onlyfiles = [f for f in listdir(file_path) if isfile(join(file_path, f))]

file_paths = [f"/home/cdsw/output/crawled_outputs/{elem}" for elem  in onlyfiles]

for f_path in file_paths:
	subprocess.call([f'hadoop fs -copyFromLocal {f_path}  hdfs:///user/dyao/'], shell=True)
	print(f"{f_path} finished moving")
