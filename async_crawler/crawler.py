import asyncio
import aiohttp
from datetime import datetime
from aiohttp import ClientSession
from typing import Dict, Union, List
import ssl
import certifi
import functools
from aiologger import Logger
from aiohttp import ClientConnectionError, ClientOSError, ClientConnectorError, ServerConnectionError, ClientSSLError, ClientConnectorSSLError, ClientConnectorCertificateError, ServerDisconnectedError, ServerTimeoutError, ServerFingerprintMismatch


def log(func):
    def decorate_log(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger_params = [elem for elem in args if isinstance(
                elem, Logger)] + [elem for elem in kwargs.values() if isinstance(elem, Logger)]
            f_logger = next(iter(logger_params))
            url_params = [elem for elm in args if isinstance(
                elem, dict)] + [elem for elem in kwargs.values() if isinstance(elem, dict)]
            f_url = next(iter(url_params))
            try:
                result = func(*args, **kwargs)
                f_logger.debug(
                    f"{result['url_id']} status code is {result['status']}")
                return result
            except Exception as e:
                f_logger.error(
                    f"{f_url['url_id']} error happened, error is {str(e)}")
                return {"url_id": f_url["url_id"], "status": 0, "html": str(e)}
        return wrapper
    return decorate_log


async def crawl(session: ClientSession, url: Dict[str, str], logger: Logger) -> Dict[str, Union[str, int]]:
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36'
    }
    try:
        async with session.get(url['url'], headers=headers, max_redirects=30) as resp:
            await logger.info(f"{url['url_id']} status code is {resp.status}, destination url is {resp.url.human_repr()}")
            html = await resp.text("utf-8", "ignore")
            return {"url_id": url["url_id"], 
                    "status": resp.status, 
                    "html": html,
                    "destination_url": resp.url.human_repr()}
    except ServerConnectionError as e:
        error_message = str(e).replace('\n', ' ')
        await logger.error(f"{url['url_id']} error happend, error is {error_message}")
        return {"url_id": url["url_id"], "status": -1, "html": error_message, "destination_url": ""}
    except ServerDisconnectedError as e:
        error_message = str(e).replace('\n', ' ')
        await logger.error(f"{url['url_id']} error happend, error is {error_message}")
        return {"url_id": url["url_id"], "status": -2, "html": error_message, "destination_url": ""}
    except ClientConnectorCertificateError as e:
        error_message = str(e).replace('\n', ' ')
        await logger.error(f"{url['url_id']} error happend, error is {error_message}")
        return {"url_id": url["url_id"], "status": -3, "html": error_message, "destination_url": ""}
    except ClientConnectorSSLError as e:
        error_message = str(e).replace('\n', ' ')
        await logger.error(f"{url['url_id']} error happend, error is {error_message}")
        return {"url_id": url["url_id"], "status": -4, "html": error_message, "destination_url": ""}
    except ClientSSLError as e:
        error_message = str(e).replace('\n', ' ')
        await logger.error(f"{url['url_id']} error happend, error is {error_message}")
        return {"url_id": url["url_id"], "status": -5, "html": error_message, "destination_url": ""}
    except ClientConnectionError as e:
        error_message = str(e).replace('\n', ' ')
        await logger.error(f"{url['url_id']} error happend, error is {error_message}")
        return {"url_id": url["url_id"], "status": -6, "html": error_message, "destination_url": ""}
    except ClientConnectorError as e:
        error_message = str(e).replace('\n', ' ')
        await logger.error(f"{url['url_id']} error happend, error is {error_message}")
        return {"url_id": url["url_id"], "status": -7, "html": error_message, "destination_url": ""}
    except ClientOSError as e:
        error_message = str(e).replace('\n', ' ')
        await logger.error(f"{url['url_id']} error happend, error is {error_message}")
        return {"url_id": url["url_id"], "status": -8, "html": error_message, "destination_url": ""}
    except ServerTimeoutError as e:
        error_message = str(e).replace('\n', ' ')
        await logger.error(f"{url['url_id']} error happend, error is {error_message}")
        return {"url_id": url["url_id"], "status": -9, "html": error_message, "destination_url": ""}
    except ServerFingerprintMismatch as e:
        error_message = str(e).replace('\n', ' ')
        await logger.error(f"{url['url_id']} error happend, error is {error_message}")
        return {"url_id": url["url_id"], "status": -10, "html": error_message, "destination_url": ""}
    except Exception as e:
        error_message = str(e).replace('\n', ' ')
        await logger.error(f"{url['url_id']} error happend, error is {error_message}")
        return {"url_id": url["url_id"], "status": 0, "html": error_message, "destination_url": ""}


async def crawl_all(urls: List[Dict[str, str]], total_timeout: float, logger: Logger) -> List[Dict[str, Union[str, int]]]:
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    conn = aiohttp.TCPConnector(ssl=False, limit=200)
    timeout = aiohttp.ClientTimeout(
        total=total_timeout, sock_connect=20, sock_read=20)
    async with aiohttp.ClientSession(connector=conn, timeout=timeout) as session:
        data_all = await asyncio.gather(*[crawl(session, url, logger) for url in urls], return_exceptions=True)
        return data_all
