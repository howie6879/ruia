#!/usr/bin/env python
"""
 Created by howie.hu at 2018/7/10.
"""
import asyncio
import aiohttp

from datetime import datetime
from threading import Thread
from types import AsyncGeneratorType

from lxml import etree

from aspider.request import Request
from aspider.utils import get_logger

try:
    import uvloop

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass


class Spider:
    name = 'aspider'
    request_config = None
    request_queue = asyncio.Queue()
    start_urls = []
    all_counts, success_counts = 0, 0

    def __init__(self, loop=None):
        if not self.start_urls or not isinstance(self.start_urls, list):
            raise ValueError("Spider must have a param named start_urls, eg: start_urls = ['https://www.github.com']")
        self.logger = get_logger(name=self.name)
        self.loop = loop or asyncio.get_event_loop()

        # self.new_loop = asyncio.new_event_loop()
        # t = Thread(target=self.start_loop, args=(self.new_loop,))
        # t.setDaemon(True)
        # t.start()

    @property
    def is_running(self):
        is_running = True
        if self.request_queue.empty():
            is_running = False
        return is_running

    def e_html(self, html):
        return etree.HTML(html)

    async def parse(self, res):
        raise NotImplementedError

    # def start_loop(self, loop):
    #     asyncio.set_event_loop(loop)
    #     loop.run_forever()

    async def start_master(self):
        for url in self.start_urls:
            request_ins = Request(url=url,
                                  callback=self.parse,
                                  extra_value=getattr(self, 'extra_value', None),
                                  headers=getattr(self, 'headers', None),
                                  request_config=getattr(self, 'request_config'),
                                  request_session=getattr(self, 'request_session', None),
                                  res_type=getattr(self, 'res_type', 'text'),
                                  **getattr(self, 'kwargs', {}))
            self.request_queue.put_nowait(request_ins.fetch_callback())
        tasks = []
        while self.is_running:
            request_item = self.request_queue.get_nowait()
            tasks.append(asyncio.ensure_future(request_item))
            if self.request_queue.empty():
                done, pending = await asyncio.wait(tasks)
                self.all_counts, self.success_counts = len(tasks), len(done)
                for task in done:
                    if isinstance(task.result(), AsyncGeneratorType):
                        async for each in task.result():
                            self.request_queue.put_nowait(each.fetch_callback())

    async def start_worker(self):
        # TODO
        pass

    @classmethod
    def start(cls):
        spider_ins = cls()
        spider_ins.logger.info('Spider started!')
        start_time = datetime.now()
        try:
            spider_ins.loop.run_until_complete(spider_ins.start_master())
        except KeyboardInterrupt:
            for task in asyncio.Task.all_tasks():
                task.cancel()
            spider_ins.loop.stop()
            spider_ins.loop.run_forever()
        finally:
            end_time = datetime.now()
            spider_ins.logger.info(f'Total requests: {spider_ins.success_counts}')
            if spider_ins.all_counts - spider_ins.success_counts:
                spider_ins.logger.info(f'Failed requests: {spider_ins.all_counts - spider_ins.success_counts}')
            spider_ins.logger.info(f'Time usage: {end_time - start_time}')
            spider_ins.logger.info('Spider finished!')
            spider_ins.loop.close()
