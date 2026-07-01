import asyncio
from pyppeteer import launch
from aiologger import Logger
from pyppeteer.errors import TimeoutError
from typing import Dict, List, Union
import time
import pandas as pd

async def setup_request_interceptor(page) -> None:
        client = page._networkManager._client

        async def intercept(event) -> None:
            interception_id = event["interceptionId"]
            request = event["request"]
            url = request["url"]

            options = {"interceptionId": interception_id}
            # You can block a request like this:
            # options["errorReason"] = "BlockedByClient"
            await client.send("Network.continueInterceptedRequest", options)

        # Setup request interception for all requests.
        client.on(
            "Network.requestIntercepted",
            lambda event: client._loop.create_task(intercept(event)),
        )
        patterns = [{"urlPattern": "*"}]
        await client.send("Network.setRequestInterception", {"patterns": patterns})

class PuppeteerCralwer():
    def __init__(self, urls: List[Dict[str, Union[str, int]]]) -> None:
        self.urls = urls

    async def browser(self):
        browser = await launch(headless=True, args=['--disable-infobars', '--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu', '--user-agent"Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5"'])
        return browser

    async def get_single_url(self, browser, url: Dict[str, str]) -> Dict[str, Union[str, int]]:
        page = await browser.newPage()
        page.setDefaultNavigationTimeout(15000)
        await page.setRequestInterception(True)
        await setup_request_interceptor(page)
        try:
            res = await page.goto(url['url'], {'waitUntil' : 'networkidle2'})
            content = await page.content()
            status = res.status
            print(res.status)
            await page.close()
            return {'url_id': url['url_id'], 'status': status, 'html': content}
        except TimeoutError as e:
            print(f"{url['url']} Timeout!")
            await page.close()
            return {'url_id': url['url_id'], 'status': -1, 'html': ''}
        except Exception as e:
            error_message = str(e).replace('\n', '')
            print(error_message)
            await page.close()
            return {'url_id': url['url_id'], 'status': 0, 'html': error_message}

    async def crawl_all(self) -> List[Dict[str, Union[str, int]]]:
        browser = await self.browser()
        tasks = [self.get_single_url(browser, url) for url in self.urls]
        result = await asyncio.gather(*tasks, return_exceptions=True)
        await browser.close()
        return result




urls_df = pd.read_csv("test_samples.csv", encoding="utf-8")
urls_df['url'] = urls_df['url'].apply(lambda x: str(x))
urls = urls_df[['url_id', 'url']].to_dict('index')
url_list = [urls[key] for key in urls.keys()]
#    urls = [{'url_id': '1', 'url': 'sms:?&body=https%3A%2F%2Fwww.dr-doerfer.de%2Fzfa-fuer-kfo-gesucht-mw-in-berlin-friedrichshain%2F'},
#            {'url_id': '2', 'url': 'https://www.ctk.de/klinikum/kliniken-zentren/kliniken/klinikum/kliniken-zentren/kliniken/orthopaedie/klinikum/kliniken-zentren/kliniken/nuklearmedizin/behandlungsspektrum.html'}]
#urls = [{'url_id': '1', 'url': 'http://www.apotheken-umschau.de/gesund-bleiben/ernaehrung/rezepte/beeriger-gartensalat-815073.html'},]
crawler = PuppeteerCralwer(url_list)
loop = asyncio.get_event_loop()
start = time.time()
a = loop.run_until_complete(crawler.crawl_all())
end = time.time()
print(end-start)
