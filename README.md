# Instpool Google API Search & URL Webcrawl

![wordcloud](figures/wordcloud_praxis.png)

This project consists of two main parts:

* **Google API** - Process that uses basic institution information to request the same and additional details from the Google Places API. The aim is to expand the URL coverage to be used for crawling. Other details can be readily used in physician or pharmacy PST.

* **Webcrawling** - Process that uses the updated URLs from the Google API to crawl the underlying websites and corresponding subpages, and stores the content in Hadoop for keyword identification / text mining to provide additional features for physician or pharmacy PST purposes.

___

## Google API

This is an implementation of a Google Places API tool that retrieves fields of interest from OneKey Instpool entries. See `futils.py` for a detailed list of fields available.

In a nutshell, the process comprises:

1. Searching places using the OneKey institution name and address as a single string (e.g. `Dr. Fink Basselstr. 21 51233 Berlin Germany`) and returning the first - if any - result

2. Use the place ID returned in 1. to request specific fields / details (e.g. `website`, `rating`, `reviews`)

3. Combine that information with other Instpool descriptors

### Instructions

Succintly, in order to use the Google API tool the following steps must be taken:

1. Get hold of an enterprise Google Cloud Platform account using your IQVIA e-mail address, create a project and fill in your billing details. Prior to any charges you will likely benefit from monthly free credit (~300EUR). Consider setting a budget limit to prevent overspending.

2. Generate a Google Places API key and make it available to `futils.py` as a one-liner stored in `.b64key`, as a base64 or similar encoding.

3. Make sure the backup folder `backup/` is empty (save for a `.gitkeep`). A backup mechanism is in place to prevent any data losses due to any eventual interruptions. Should that happen, re-running `futils.full_processing()` will load the backup results, search the remaining institutions and return the full set.

4. Specify `COUNTRY` in `futils.py` (e.g. Germany) to restrict searches to a country of interest. Also, define `desc` in `0_search_api.py`, a list of descriptors from the input table (e.g. institution name, address, ZIP code) to be searched against.

For extensive documentation about the Google Places API please refer to the corresponding [page in the Google Maps Platform](https://developers.google.com/maps/documentation/places/web-service/overview).

### Costs

All requests done via `futils.get_place_id()` are free-of-charge. On the other hand, the cost of requests passed via `futils.get_details()` will depend on

* Types of data in scope - Basic, Contacts, Atmosphere
* Monthly volume of requests - >100,000 requests / month are subject to ~20% discount
* Returning at least one result - if no `place_id` is returned, no details need to be searched

 This project was associated with the following pricing scheme:

| SKU description      | Per unit quantity | Tiered usage start | List price (EUR) |
| -------------------- | ----------------- | ------------------ | ---------------- |
| Find Place - ID only | 1                 | 0                  | 0                | 
| Places Details       | 1000              | 0                  | 15.2320          |
| Places Details       | 1000              | 100,000            | 12.1856          |
| Basic Data           | 1                 | 0                  | 0                |
| Contact Data         | 1000              | 0                  | 2.6880           |
| Contact Data         | 1000              | 100,000            | 2.1504           |
| Atmosphere Data      | 1000              | 0                  | 4.4800           |
| Atmosphere Data      | 1000              | 100,000            | 3.5840           |

Note that Basic data are included in the base Place Details request; if Contact and / or Atmosphere data are added on top, the provided charges apply. Keep in mind overall costs are buffered by the monthly free credit aforementioned. Prices might change, so plan the scope of requests at your own discretion.

___

## Webcrawling

This part aims to collect a rich set of information online based on results generated from [Google API](#google-api). 

A "bootstrap" method is used to scrape websites and subpages, in order to control the level of depth on information needed.

Specifically, the methodology contains the following procedures:

1. Crawl all URLs from [Google API](#google-api) or URLs from last round of crawling, output them as format of HTML contents
2. Parse the HTML contents from step 1, and extract all links
3. Filter out HTTP(S) hyperlinks from step 2, save them as the URL list for the next round
4. Repeat step 1, 2, and 3 to gain one more level of depth

Level of depth is chosen based on the tradeoff between relevance and completeness of information scraped.

### Instructions

Implementation of crawler and post-processing of html contents is placed in `~/async_crawler`.

* Crawler\
The entry point to start the crawler program is `~/async_crawler/crawler_starter.py`. A number of command-line arguments are required to start the crawler. Please type `crawler_starter.py --help` in terminal to see the detailed explanations of arguments. Particularly, the program needs a URL list as input to be crawled. It has to be in format of parquet and must contain two fields, `url` and `url_id`. The `url_id` is MD5 of URL as a string.

* Extraction of links\
The implementation is in `~/async_crawler/analyze_html_links.py`. The program requires a list of Hadoop file paths as inputs, which points to the HTML content data files. It will extract all links from HTML contents and label their types (HTTP link, javascript, anchor, and telephone). The link is defined as `href` attribute enveloped in `<a>` tag in HTML.
