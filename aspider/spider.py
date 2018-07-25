#!/usr/bin/env python

import asyncio
import aiohttp

from datetime import datetime
from types import AsyncGeneratorType

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

    failed_counts, success_counts = 0, 0
    start_urls, worker_tasks = [], []

    def __init__(self, loop=None):
        if not self.start_urls or not isinstance(self.start_urls, list):
            raise ValueError("Spider must have a param named start_urls, eg: start_urls = ['https://www.github.com']")
        self.logger = get_logger(name=self.name)
        self.loop = loop or asyncio.get_event_loop()
        self.sem = asyncio.Semaphore(getattr(self, 'concurrency', 3))

    async def parse(self, res):
        raise NotImplementedError

    async def start_master(self):
        for url in self.start_urls:
            request_ins = Request(url=url,
                                  callback=self.parse,
                                  metadata=getattr(self, 'metadata', None),
                                  headers=getattr(self, 'headers', None),
                                  request_config=getattr(self, 'request_config'),
                                  request_session=getattr(self, 'request_session', None),
                                  res_type=getattr(self, 'res_type', 'text'),
                                  **getattr(self, 'kwargs', {}))
            self.request_queue.put_nowait(request_ins.fetch_callback(self.sem))
        workers = [asyncio.ensure_future(self.start_worker()) for i in range(2)]
        await self.request_queue.join()
        for work in workers:
            work.cancel()

    async def start_worker(self):
        while True:
            request_item = await self.request_queue.get()
            self.worker_tasks.append(asyncio.ensure_future(request_item))
            if self.request_queue.empty():
                done, pending = await asyncio.wait(self.worker_tasks)
                for task in done:
                    callback_res, res = task.result()
                    if isinstance(callback_res, AsyncGeneratorType):
                        async for each in callback_res:
                            self.request_queue.put_nowait(each.fetch_callback(self.sem))
                    if res.body is None:
                        self.failed_counts += 1
                    else:
                        self.success_counts += 1
                self.worker_tasks = []
            self.request_queue.task_done()

    def make_request_from_url(self, url):
        yield Request(url=url)

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
            spider_ins.logger.info(f'Total requests: {spider_ins.failed_counts + spider_ins.success_counts}')
            if spider_ins.failed_counts:
                spider_ins.logger.info(f'Failed requests: {spider_ins.failed_counts}')
            spider_ins.logger.info(f'Time usage: {end_time - start_time}')
            spider_ins.logger.info('Spider finished!')
            spider_ins.loop.close()
