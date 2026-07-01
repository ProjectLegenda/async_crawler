import pandas as pd
from collections import Counter


def categorize_level(merge_type: str) -> str:
    if merge_type == "left_only":
        result = "level_0"
    elif merge_type == "right_only":
        result = "level_1"
    elif merge_type == "both":
        result = "level_0|level_1"
    return result


level0 = pd.read_parquet("/home/cdsw/output/crawled_outputs/T_URL.parquet")

level0 = level0[['url_id', 'url']]

level0['page_type'] = 'http link'

level1 = pd.read_parquet(
    "/home/cdsw/output/crawled_outputs/T_URL_depth1.parquet")

level_0_1 = pd.merge(level0, level1, on=[
                     'url_id', 'url', 'page_type'], how='outer', indicator=True)

level_0_1['level'] = level_0_1['_merge'].apply(lambda x: categorize_level(x))

level_0_1 = level_0_1[['url_id', 'url', 'page_type', 'level']]

level_0_1.to_parquet(
    "/home/cdsw/output/crawled_outputs/T_URL_0_depth1.parquet")
