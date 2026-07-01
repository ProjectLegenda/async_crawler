from asyncio.unix_events import _UnixSelectorEventLoop
import os
import sys
import datetime
import asyncio

from aiologger import Logger
from aiologger.utils import bind_loop
from aiologger.levels import LogLevel
from aiologger.formatters.base import Formatter
from aiologger.handlers.files import AsyncFileHandler
from aiologger.handlers.streams import AsyncStreamHandler


class AsyncLogger(object):
    def __init__(self, name: str = None, loop: _UnixSelectorEventLoop = None) -> None:
        day_date = datetime.datetime.now().strftime("%Y-%m-%d")
        log_path = f"logs/{day_date}"

        if not os.path.exists(log_path):
            os.makedirs(log_path)

        if loop is None:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        self.loop = loop

        formatter = Formatter(
            '[%(asctime)s] %(filename)s -> %(funcName)s line:%(lineno)d [%(levelname)s] %(message)s')

        logger = Logger(name=name, level=LogLevel.INFO)

#        ash = bind_loop(AsyncStreamHandler, {})(stream=sys.stderr,
#                                                level=LogLevel.INFO, formatter=formatter)
#
#        logger.add_handler(ash)

        log_name = f"{log_path}{name}.log"
        afh = AsyncFileHandler(log_name, 'a', encoding='utf-8')
        afh.formatter = formatter

        self.logger = logger
        self.logger.add_handler(afh)

    def get_logger(self) -> Logger:
        return self.logger
