#!/usr/bin/env python

import collections
import asyncio
import typing

from datetime import datetime
from functools import reduce
from inspect import isawaitable
from signal import SIGINT, SIGTERM
from types import AsyncGeneratorType

from ruia.middleware import Middleware
from ruia.request import Request
from ruia.response import Response
from ruia.utils import get_logger

try:
    import uvloop

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass


class Spider:
    name = 'ruia'  # Used for log
    request_config = None
    request_session = None

    # Default values passing to each request object. Not implemented yet.
    headers: dict = None
    metadata: dict = None
    kwargs: dict = None

    res_type: str = 'text'

    # Some fields for statistics
    failed_counts: int = 0
    success_counts: int = 0

    # Concurrency control
    concurrency: int = 3

    # Spider entry
    start_urls: list = None

    # A queue to save coroutines
    worker_tasks: list = []

    def __init__(self,
                 middleware: typing.Union[typing.Iterable, Middleware] = None,
                 loop=None,
                 is_async_start: bool = False):
        """
        Init spider object.
        :param middleware: a list of or a single Middleware
        :param loop:
        :param is_async_start:
        """
        if not self.start_urls or not isinstance(self.start_urls, collections.Iterable):
            raise ValueError("Spider must have a param named start_urls, eg: start_urls = ['https://www.github.com']")
        # Init object-level properties
        if self.request_config is None:
            self.request_config = dict()
        if self.headers is None:
            self.headers = dict()
        if self.metadata is None:
            self.metadata = dict()
        if self.kwargs is None:
            self.kwargs = dict()
        if self.start_urls is None:
            self.start_urls = list()

        self.is_async_start = is_async_start
        self.logger = get_logger(name=self.name)
        self.loop = loop
        asyncio.set_event_loop(self.loop)

        # customize middleware
        if isinstance(middleware, list):
            self.middleware = reduce(lambda x, y: x + y, middleware)
        else:
            self.middleware = middleware or Middleware()

        # async queue as a producer
        self.request_queue = asyncio.Queue()

        # semaphore, used for concurrency control
        self.sem = asyncio.Semaphore(self.concurrency)

    async def parse(self, res: Response):
        """
        Used for subclasses, directly parse the responses corresponding with start_urls
        :param res: Response
        :return:
        """
        raise NotImplementedError

    @classmethod
    async def async_start(cls,
                          middleware: Middleware = None,
                          loop=None,
                          after_start=None,
                          before_stop=None):
        """
        Start an async spider
        :param middleware:
        :param loop:
        :param after_start:
        :param before_stop:
        :return:
        """
        loop = loop or asyncio.get_event_loop()
        spider_ins = cls(middleware=middleware, loop=loop, is_async_start=True)
        spider_ins.logger.info('Spider started!')
        start_time = datetime.now()

        # Run hook before spider start crawling
        if after_start:
            assert callable(after_start)
            coroutine_after_start = after_start(spider_ins)
            assert isawaitable(coroutine_after_start)
            await coroutine_after_start

        # Actually run crawling
        try:
            await spider_ins.start_master()
        finally:

            # Run hook after spider finished crawling
            if before_stop:
                assert callable(before_stop)
                coroutine_before_stop = before_stop(spider_ins)
                assert isawaitable(coroutine_before_stop)
                await coroutine_before_stop

            # Display logs about this crawl task
            end_time = datetime.now()
            spider_ins.logger.info(f'Total requests: {spider_ins.failed_counts + spider_ins.success_counts}')
            if spider_ins.failed_counts:
                spider_ins.logger.info(f'Failed requests: {spider_ins.failed_counts}')
            spider_ins.logger.info(f'Time usage: {end_time - start_time}')
            spider_ins.logger.info('Spider finished!')

    @classmethod
    def start(cls, middleware=None, loop=None, after_start=None, before_stop=None, close_event_loop=True):
        """
        Start a spider
        :param after_start: hook
        :param before_stop: hook
        :param middleware: customize middleware or a list of middleware
        :param loop: event loop
        :param close_event_loop: bool
        :return:
        """
        loop = loop or asyncio.new_event_loop()
        spider_ins = cls(middleware=middleware, loop=loop)
        spider_ins.is_async_start = False
        spider_ins.logger.info('Spider started!')
        start_time = datetime.now()

        # Hook
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
        # Actually start crawling
        asyncio.ensure_future(spider_ins.start_master())

        try:
            spider_ins.loop.run_forever()
        finally:

            # hook
            if before_stop:
                assert callable(before_stop)
                coroutine_before_stop = before_stop(spider_ins)
                assert isawaitable(coroutine_before_stop)
                spider_ins.loop.run_until_complete(coroutine_before_stop)

            # Log for this crawling task
            end_time = datetime.now()
            spider_ins.logger.info(f'Total requests: {spider_ins.failed_counts + spider_ins.success_counts}')
            if spider_ins.failed_counts:
                spider_ins.logger.info(f'Failed requests: {spider_ins.failed_counts}')
            spider_ins.logger.info(f'Time usage: {end_time - start_time}')
            spider_ins.logger.info('Spider finished!')
            spider_ins.loop.run_until_complete(spider_ins.loop.shutdown_asyncgens())
            if close_event_loop:
                spider_ins.loop.close()

    async def handle_request(self, request: Request) -> typing.Tuple[AsyncGeneratorType, Response]:
        """
        Wrap request with middlewares.
        :param request:
        :return:
        """
        await self._run_request_middleware(request)
        callback_result, response = await request.fetch_callback(self.sem)  # sem is used for concurrency control
        await self._run_response_middleware(request, response)
        return callback_result, response

    async def start_master(self):
        """Actually start crawling."""
        for url in self.start_urls:
            request_ins = Request(url=url,
                                  callback=self.parse,
                                  headers=self.headers.copy(),
                                  metadata=self.metadata.copy(),
                                  request_config=self.request_config.copy(),
                                  request_session=self.request_session,
                                  res_type=self.res_type,
                                  **self.kwargs.copy())
            self.request_queue.put_nowait(self.handle_request(request_ins))
        tasks = [asyncio.ensure_future(self.start_worker()) for i in range(2)]
        await self.request_queue.join()
        if not self.is_async_start:
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
        """
        Finish all running tasks, cancel remaining tasks, then stop loop.
        :param _signal:
        :return:
        """
        self.logger.info(f'Stopping spider: {self.name}')
        tasks = [task for task in asyncio.Task.all_tasks() if task is not
                 asyncio.tasks.Task.current_task()]
        [task.cancel() for task in tasks]
        await asyncio.gather(*tasks, return_exceptions=True)
        self.loop.stop()

    async def _run_request_middleware(self, request):
        if self.middleware.request_middleware:
            for middleware in self.middleware.request_middleware:
                middleware_coroutine = middleware(request)
                if isawaitable(middleware_coroutine):
                    try:
                        await middleware_coroutine
                    except Exception as e:
                        self.logger.exception(e)
                else:
                    self.logger.error('Middleware must be a coroutine function')

    async def _run_response_middleware(self, request, response):
        if self.middleware.response_middleware:
            for middleware in self.middleware.response_middleware:
                middleware_coroutine = middleware(request, response)
                if isawaitable(middleware_coroutine):
                    try:
                        await middleware_coroutine
                    except Exception as e:
                        self.logger.exception(e)
                else:
                    self.logger.error('Middleware must be a coroutine function')
