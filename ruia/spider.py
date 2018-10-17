#!/usr/bin/env python

import asyncio

from datetime import datetime
from functools import reduce
from inspect import isawaitable
from signal import SIGINT, SIGTERM
from types import AsyncGeneratorType

from ruia.middleware import Middleware
from ruia.request import Request
from ruia.utils import get_logger

try:
    import uvloop

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass


class Spider:
    name = 'ruia'
    request_config = None

    failed_counts, success_counts = 0, 0
    start_urls, worker_tasks = [], []

    def __init__(self, middleware=None, loop=None):
        if not self.start_urls or not isinstance(self.start_urls, list):
            raise ValueError("Spider must have a param named start_urls, eg: start_urls = ['https://www.github.com']")
        self.logger = get_logger(name=self.name)
        self.loop = loop or asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        # customize middleware
        if isinstance(middleware, list):
            self.middleware = reduce(lambda x, y: x + y, middleware)
        else:
            self.middleware = middleware or Middleware()
        # async queue
        self.request_queue = asyncio.Queue()
        # semaphore
        self.sem = asyncio.Semaphore(getattr(self, 'concurrency', 3))

    async def parse(self, res):
        raise NotImplementedError

    @classmethod
    def start(cls, after_start=None, before_stop=None, middleware=None, loop=None, close_event_loop=True):
        """
        Start a spider
        :param after_start:
        :param before_stop:
        :param middleware: customize middleware or a list of middleware
        :param loop: event loop
        :return:
        """
        spider_ins = cls(middleware=middleware, loop=loop)
        spider_ins.logger.info('Spider started!')
        start_time = datetime.now()

        if after_start:
            func_after_start = after_start(spider_ins)
            if isawaitable(func_after_start):
                spider_ins.loop.run_until_complete(func_after_start)

        for _signal in (SIGINT, SIGTERM):
            try:
                spider_ins.loop.add_signal_handler(_signal, lambda: asyncio.ensure_future(spider_ins.stop(_signal)))
            except NotImplementedError:
                spider_ins.logger.warning(f'{spider_ins.name} tried to use loop.add_signal_handler '
                                          'but it is not implemented on this platform.')
        asyncio.ensure_future(spider_ins.start_master())
        try:
            spider_ins.loop.run_forever()
        finally:
            if before_stop:
                func_before_stop = before_stop(spider_ins)
                if isawaitable(func_before_stop):
                    spider_ins.loop.run_until_complete(func_before_stop)

            end_time = datetime.now()
            spider_ins.logger.info(f'Total requests: {spider_ins.failed_counts + spider_ins.success_counts}')
            if spider_ins.failed_counts:
                spider_ins.logger.info(f'Failed requests: {spider_ins.failed_counts}')
            spider_ins.logger.info(f'Time usage: {end_time - start_time}')
            spider_ins.logger.info('Spider finished!')
            spider_ins.loop.run_until_complete(spider_ins.loop.shutdown_asyncgens())
            if close_event_loop:
                spider_ins.loop.close()

    async def handle_request(self, request):
        # request middleware
        await self._run_request_middleware(request)
        # make a request
        callback_res, response = await request.fetch_callback(self.sem)
        # response middleware
        await self._run_response_middleware(request, response)
        return callback_res, response

    async def start_master(self):
        for url in self.start_urls:
            request_ins = Request(url=url,
                                  callback=self.parse,
                                  headers=getattr(self, 'headers', {}),
                                  load_js=getattr(self, 'load_js', False),
                                  metadata=getattr(self, 'metadata', {}),
                                  request_config=getattr(self, 'request_config'),
                                  request_session=getattr(self, 'request_session', None),
                                  res_type=getattr(self, 'res_type', 'text'),
                                  **getattr(self, 'kwargs', {}))
            # self.request_queue.put_nowait(request_ins.fetch_callback(self.sem))
            self.request_queue.put_nowait(self.handle_request(request_ins))
        workers = [asyncio.ensure_future(self.start_worker()) for i in range(2)]
        await self.request_queue.join()
        await self.stop(SIGINT)

    async def start_worker(self):
        while True:
            request_item = await self.request_queue.get()
            self.worker_tasks.append(request_item)
            if self.request_queue.empty():
                results = await asyncio.gather(*self.worker_tasks, return_exceptions=True)
                for task_result in results:
                    if not isinstance(task_result, RuntimeError):
                        callback_res, res = task_result
                        if isinstance(callback_res, AsyncGeneratorType):
                            async for request_ins in callback_res:
                                self.request_queue.put_nowait(self.handle_request(request_ins))
                        if res.html is None:
                            self.failed_counts += 1
                        else:
                            self.success_counts += 1
                self.worker_tasks = []
            self.request_queue.task_done()

    async def stop(self, _signal):
        self.logger.info(f'Stopping spider: {self.name}')
        tasks = [task for task in asyncio.Task.all_tasks() if task is not
                 asyncio.tasks.Task.current_task()]
        list(map(lambda task: task.cancel(), tasks))
        results = await asyncio.gather(*tasks, return_exceptions=True)
        self.loop.stop()

    async def _run_request_middleware(self, request):
        if self.middleware.request_middleware:
            for middleware in self.middleware.request_middleware:
                middleware_func = middleware(request)
                if isawaitable(middleware_func):
                    try:
                        result = await middleware_func
                    except Exception as e:
                        self.logger.exception(e)
                else:
                    self.logger.error('Middleware must be a coroutine function')
                    result = None

    async def _run_response_middleware(self, request, response):
        if self.middleware.response_middleware:
            for middleware in self.middleware.response_middleware:
                middleware_func = middleware(request, response)
                if isawaitable(middleware_func):
                    try:
                        result = await middleware_func
                    except Exception as e:
                        self.logger.exception(e)
                else:
                    self.logger.error('Middleware must be a coroutine function')
                    result = None
