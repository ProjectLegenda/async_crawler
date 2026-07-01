import pandas as pd
import dask.dataframe as dd
from utils import get_hrefs, generate_href_edge
import time
import itertools


if __name__ == "__main__":
    url = pd.read_parquet("/home/cdsw/output/crawled_outputs/T_URL_depth1.parquet")
    subpages = []
    edges = []
    start = time.time()
    for i in range(277):
        data = pd.read_parquet(
            f"/home/cdsw/output/crawled_outputs/crawled_html_chunk_{i+17}.parquet")

        data = data[data['status'] == 200]

        data = data.merge(url, how="left", on="url_id")

        ddata = dd.from_pandas(data, npartitions=100)

        res = ddata.map_partitions(lambda df: df.apply(
            (lambda row: get_hrefs(str(row['html']), str(row['url']), str(row['url_id']))), axis=1)).compute(scheduler="processes").tolist()
        subpages_url = list(itertools.chain.from_iterable(
            [elem['subpages'] for elem in res]))
        ed = list(itertools.chain.from_iterable(
            [generate_href_edge(elem) for elem in res]))
        subpages += subpages_url
        edges += ed

    end = time.time()

    print(f"elapsed time is {end-start} seconds")

    del data
    del res
    del subpages_url
    subpages_df = pd.DataFrame(subpages)
    edges_df = pd.DataFrame(edges)
    subpages_df.drop_duplicates(inplace=True)
    edges_df.drop_duplicates(inplace=True)
    http_subpages = subpages_df[subpages_df['page_type'] == "http link"]
    print(f"number of subpages is {len(subpages_df)}")
    print(f"number of http subpages is {len(http_subpages)}")
    print(f"number of edges is {len(edges)}")
    subpages_df.to_parquet(
        "/home/cdsw/output/crawled_outputs/T_URL_depth2.parquet", index=False)
    edges_df.to_parquet(
        "/home/cdsw/output/crawled_outputs/link_relations_depth1.parquet", index=False)
