#!/usr/bin/env python

import asyncio
import collections
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
    """
    Spider is used for control requests better
    """

    name = 'ruia'
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
    worker_numbers: int = 2
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
        self.request_config = self.request_config or {}
        self.headers = self.headers or {}
        self.metadata = self.metadata or {}
        self.kwargs = self.kwargs or {}
        self.request_config = self.request_config or {}

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

    async def parse(self, response: Response):
        """
        Used for subclasses, directly parse the responses corresponding with start_urls
        :param response: Response
        :return:
        """
        raise NotImplementedError

    async def _start(self, after_start=None, before_stop=None):
        self.logger.info('Spider started!')
        start_time = datetime.now()

        # Run hook before spider start crawling
        await self._run_spider_hook(after_start)

        # Actually run crawling
        try:
            await self.start_master()
        finally:
            # Run hook after spider finished crawling
            await self._run_spider_hook(before_stop)
            # Display logs about this crawl task
            end_time = datetime.now()
            self.logger.info(f'Total requests: {self.failed_counts + self.success_counts}')
            if self.failed_counts:
                self.logger.info(f'Failed requests: {self.failed_counts}')
            self.logger.info(f'Time usage: {end_time - start_time}')
            self.logger.info('Spider finished!')

    @classmethod
    async def async_start(cls,
                          middleware: typing.Union[typing.Iterable, Middleware] = None,
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
        await spider_ins._start(after_start=after_start, before_stop=before_stop)

    @classmethod
    def start(cls,
              middleware: typing.Union[typing.Iterable, Middleware] = None,
              loop=None,
              after_start=None,
              before_stop=None,
              close_event_loop=True):
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

        for signal in (SIGINT, SIGTERM):
            try:
                spider_ins.loop.add_signal_handler(signal, lambda: asyncio.ensure_future(spider_ins.stop(signal)))
            except NotImplementedError:
                spider_ins.logger.warning(f'{spider_ins.name} tried to use loop.add_signal_handler '
                                          'but it is not implemented on this platform.')
        # Actually start crawling
        spider_ins.loop.run_until_complete(spider_ins._start(after_start=after_start, before_stop=before_stop))
        spider_ins.loop.run_until_complete(spider_ins.loop.shutdown_asyncgens())
        if close_event_loop:
            spider_ins.loop.close()

    async def handle_callback(self, callback_func, response):
        callback_result = await callback_func
        return callback_result, response

    async def handle_request(self, request: Request) -> typing.Tuple[AsyncGeneratorType, Response]:
        """
        Wrap request with middlewares.
        :param request:
        :return:
        """
        await self._run_request_middleware(request)
        # sem is used for concurrency control
        callback_result, response = await request.fetch_callback(self.sem)
        await self._run_response_middleware(request, response)
        return callback_result, response

    async def multiple_request(self, url_config_list):
        """For crawling multiple urls"""
        results = await asyncio.gather(*[self.request(**url_config).fetch() for url_config in url_config_list],
                                       return_exceptions=True)
        for task_result in results:
            if not isinstance(task_result, RuntimeError) and task_result:
                yield task_result

    def request(self, url: str, method: str = 'GET', *,
                callback=None,
                encoding: typing.Optional[str] = None,
                headers: dict = None,
                metadata: dict = None,
                request_config: dict = None,
                request_session=None,
                res_type: str = None,
                **kwargs):
        """Init a Request class for crawling html"""
        headers = headers or {}
        metadata = metadata or {}
        request_config = request_config or {}
        request_session = request_session or self.request_session
        res_type = res_type or self.res_type

        headers.update(self.headers.copy())
        request_config.update(self.request_config.copy())
        kwargs.update(self.kwargs.copy())

        return Request(url=url,
                       method=method,
                       callback=callback,
                       encoding=encoding,
                       headers=headers,
                       metadata=metadata,
                       request_config=request_config,
                       request_session=request_session,
                       res_type=res_type,
                       **kwargs)

    async def start_master(self):
        """Actually start crawling."""
        for url in self.start_urls:
            request_ins = self.request(url=url, callback=self.parse, metadata=self.metadata)
            self.request_queue.put_nowait(self.handle_request(request_ins))
        [asyncio.ensure_future(self.start_worker()) for i in range(self.worker_numbers)]
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
                    if not isinstance(task_result, RuntimeError) and task_result:
                        callback_result, response = task_result
                        if isinstance(callback_result, AsyncGeneratorType):
                            async for callback_ins in callback_result:
                                if isinstance(callback_ins, Request):
                                    self.request_queue.put_nowait(self.handle_request(callback_ins))
                                else:
                                    self.request_queue.put_nowait(self.handle_callback(callback_ins, response))
                        if response.html is None:
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
                middleware_aws = middleware(request)
                if isawaitable(middleware_aws):
                    try:
                        await middleware_aws
                    except Exception as e:
                        self.logger.exception(e)
                else:
                    self.logger.error('Middleware must be a coroutine function')

    async def _run_response_middleware(self, request, response):
        if self.middleware.response_middleware:
            for middleware in self.middleware.response_middleware:
                middleware_aws = middleware(request, response)
                if isawaitable(middleware_aws):
                    try:
                        await middleware_aws
                    except Exception as e:
                        self.logger.exception(e)
                else:
                    self.logger.error('Middleware must be a coroutine function')

    async def _run_spider_hook(self, hook_func):
        if callable(hook_func):
            aws_hook_func = hook_func(self)
            if isawaitable(aws_hook_func):
                try:
                    await aws_hook_func
                except Exception as e:
                    self.logger.exception(e)
            else:
                self.logger.error("Spider's hook must be a coroutine function")
