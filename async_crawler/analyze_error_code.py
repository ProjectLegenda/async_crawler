import pandas as pd
from collections import Counter

error_list= []

for i in range(14):
	df = pd.read_parquet(f"/home/cdsw/output/crawled_outputs/crawled_html_chunk_{280+i}.parquet")
	df = df[df['status'] != 200]
	errors = df['status'].tolist()
	error_list += errors

results = Counter(error_list)
results_df = pd.DataFrame.from_dict(results, orient="index")
results_df.to_csv("stats.csv", sep=",")
