import pandas as pd

level0 = pd.read_parquet("/home/cdsw/output/crawled_outputs/T_URL.parquet")

level0 = level0[['url_id', 'url']]

level0['page_type'] = 'http link'

level1 = pd.read_parquet("/home/cdsw/output/crawled_outputs/T_URL_depth1.parquet")

all_URL = pd.merge(level1, level0, on=['url_id', 'url', 'page_type'], how='outer', indicator=True)

all_URL = all_URL[all_URL['_merge'] == 'left_only']

all_URL = all_URL[all_URL['page_type'] == 'http link']

all_URL = all_URL[['url_id', 'url']]

all_URL.to_parquet("/home/cdsw/output/crawled_outputs/T_URL_depth1_wo_overlap.parquet", index=False)
