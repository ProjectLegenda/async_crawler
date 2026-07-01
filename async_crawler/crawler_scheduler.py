import subprocess
import shlex
import time


def execute_crawler_job(url_data_name: str, url_chunk_num: int, file_chunk_num: int) -> None:
    cmd = f"python3 crawler_starter.py --url_path=hdfs:///user/dyao/{url_data_name} --url_chunk_num={url_chunk_num} --file_chunk_num={file_chunk_num}"
    subprocess.call(shlex.split(cmd), shell=False)


if __name__ == "__main__":
#    crawled_list = [2624, 2635, 2637, 2642, 2649, 2651, 2665]
    crawled_list = [i + 1 for i in range(14)]
    index_list = [elem for elem in crawled_list]
    for i, j in zip(index_list, crawled_list):
        execute_crawler_job("T_URL.parquet", i, j)
        time.sleep(30)
