Implementation of crawler and HTML analysis for Instpool URL
============================================================

# Introduction

This code base aims to implement the crawling of Instpool URLs, analysis of their HTML contents, persistence of data in BDF in an effective way.

With a set of URLs as initial seeds, the implementation is able to execute the crawling and analysis to any depth in an iterative way.

Specifically, starting from a set of seed URLs (level 0), the crawler will crawl them, get their HTML contents. Then the analyzer will extract links from contents as level 1 URLs for the next round of crawling. The procedures can be called iteratively.

# Methodology

Since the implementation is involved in both CPU bound and IO bound task, they are handled separately. 

For crawling, which is IO bound, the implementation leverages the Python coroutine to achieve high concurrency.

For analysis of HTML contents, which is CPU bound, the implementation uses multiprocessing to achieve parallel computing.

Two modules are decoupled with each other to achieve efficiency.

# Code Structure

## `crawler.py`

This is the core module of web crawler. It contains the main implementation of asynchronous crawler.

### `crawl(session: ClientSession, url: Dict[str, str], logger: Logger)`
Atomic function to send a http request asynchronously
- `session`: an asynchronous client session used to sent http requests
- `url`: a dictionary which contains two keys: `url_id` which is the MD5 of URL, and `url` which is the text format of URL
- `logger`: an asynchronous logger to record the outcome of crawling

### `crawl_all(urls: List[Dict[str, str]], total_timeout: float, logger: Logger)`
Function to send a list of http requests asynchronously and gather the results
- `urls`: list of urls, data structure of each element should be aligned with url in `crawl`
- `total_timeout`: the maximum time (in seconds) for list of http requests processed. Please be noted that this is the total timeout, not the timeout for each request
- `logger`: an asynchronous looger to record the outcome of crawling

## `utils.py`
This is a utility module containing a set of functions to help you to setup the crawler and analyze the HTML contents

###  `hash_url(url: str)`
This is a function to generate the unique id (md5) of url. You can call this function to generate url\_id of URL.

###  `clean_data(html: str)`
This is a function to clean the crawled HTML contents by removing a set of disturbing characters. Specifically, it removes newline character, 0001 in unicode, and any bytes which cannot be decoded into UTF-8 characters.

### `get_href(html: str, url: str, url_id: str)`
This is a function used to extract links from HTML content of URL
- `html`: HTML content as as string
- `url`: URL of this HTML content
- `url_id`: MD5 of this URL

### `generate_href_edge(links_data: Dict[str, Union[str, List[Dict[str, str]]]])`
This function "flattens" the result from calling `get_href` to get parent-child relation among URLs.

## `crawler_starter.py`
This is sample module to initiate a crawler and store crawled data into Hadoop file system.

Please see in the section [How to Use It](#how-to-use-it) on how to use it.

## `crawler_scheduler.py`
This is a sample module to initiate a sequence of crawler jobs for automatic crawling.

Please see in the section [How to Use It](#how-to-use-it) on how to use it.

# How to Use It 
This section gives a brief introdction on procedures to call the core modules, for crawling, post analysis, and storage.

## Initiate a crawler job
You can directly call `crawler_starter.py` in shell to start a crawler job.

There are three command-line arguments for this module:
- url\_path: path of data of URL list, in the format of parquet. There should be at least two fields in this parquet file, `url_id` and `url`. You can call `hash_url` in `utils.py` to generate `url_id` for each URL.
- url\_chunk\_num: crawler crawls the list of data by chunk, each chunk contains 10, 000 URLs. This parameter defines the chunk number of URL list you would like to crawl. For example, if url\_chunk\_num=3, the crawler will crawl 30001:40000 of URL list. 
- file\_chunk\_num: The crawled output is also stored in chunks. This parameter sets the chunk number of output file. For example, if file\_chunk\_num=100, the output of this crawler job will be stored as a CSV file in Hadoop file system, named as `crawle_html_chunk_100.csv`.

An example of calling this module in shell is
```shell
python3 crawler_starter.py --url_path=hdfs:///user/dyao/T_URL.parquet --url_chunk_num=1 --file_chunk_num=1
```

## Initiate a sequence of crawler job
If you have a long list to crawl, it would be better to initiate a sequence of crawler job and let them execute consecutively without stop.

In such scenario, you can call `crawler_scheduler.py` to deploy those jobs. This module shows an example to call a series of shell command in Python for those tasks. You can adjust parameters in function `execute_cralwer_job` to customize your own scheduler.

## Analyze HTML contents

`analzye_html_links.py` shows a demo to extract links from HTML contents with dask and BeautifulSoup. The analysis will output two datasets, one is a URL list for the next round of iteration, the other one is the parent-child realtionship between pages.



# Crawling Output Data Structure

The crawling data output is organized as three parts:

## T\_URL\_0\_depth1
This table contains the master data of URL. Its schema is:
- url\_id (string): MD5 of URL as an unique id
- url (string): URL
- level (string): the level of URL. For example, the level of base URL is level\_0, subpage of base URL is level\_1
- page\_type (string): the type of URL will be categorized as four: a) http link b) javascript c) email d) telephone

## link\_relations
This table contains the link relations among URLs as a graph. Its schema is:
- source (string): url id of master page
- target (string): url id of subpage
A row of data in link\_relations stands for an edge between URL. Source URL A with target URL B means URL B is the subpages of URL A

## crawled\_html\_{num} (in chunks)
This table contains the html content of URLs. Its schema is:
- url\_id (string): url id of URL
- status (int): status code of http response from the URL, 0 for exception thrown from the http response
- html (string): html content as a string
