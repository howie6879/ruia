"""
    Created by howie.hu at 2018.
    Description:  Crawler startup class
    Changelog: all notable changes to this file will be documented
"""

import asyncio
import sys
import typing

try:
    # python 3.6+
    import collections.abc as collectionsAbc
except ImportError:
    import collections as collectionsAbc

from datetime import datetime
from functools import reduce
from inspect import isawaitable
from signal import SIGINT, SIGTERM
from types import AsyncGeneratorType

from aiohttp import ClientSession

from ruia.exceptions import NothingMatchedError, NotImplementedParseError
from ruia.item import Item
from ruia.middleware import Middleware
from ruia.request import Request
from ruia.response import Response
from ruia.spider_hook import SpiderHook
from ruia.utils import get_logger

if sys.version_info >= (3, 8) and sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

if sys.version_info >= (3, 9):
    async_all_tasks = asyncio.all_tasks
    async_current_task = asyncio.current_task
else:
    async_all_tasks = asyncio.Task.all_tasks
    async_current_task = asyncio.tasks.Task.current_task
try:
    import uvloop

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass


class Spider(SpiderHook):
    """
    Spider is used for control requests better
    """

    name = "Ruia"
    request_config = None

    # Default values passing to each request object. Not implemented yet.
    headers: dict = None
    metadata: dict = None
    aiohttp_kwargs: dict = None

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

    def __init__(
        self,
        middleware: typing.Union[typing.Iterable, Middleware] = None,
        loop=None,
        is_async_start: bool = False,
        cancel_tasks: bool = True,
        **spider_kwargs,
    ):
        """
        Init spider object.
        :param middleware: a list of or a single Middleware
        :param loop: asyncio event llo
        :param is_async_start: start spider by using async
        :param spider_kwargs
        """
        if not self.start_urls or not isinstance(
            self.start_urls, collectionsAbc.Iterable
        ):
            raise ValueError(
                "Ruia spider must have a param named start_urls, eg: start_urls = ['https://www.github.com']"
            )

        self.loop = loop
        asyncio.set_event_loop(self.loop)

        # Init object-level properties
        self.callback_result_map = self.callback_result_map or {}
        self.request_config = self.request_config or {}
        self.headers = self.headers or {}
        self.metadata = self.metadata or {}
        self.aiohttp_kwargs = self.aiohttp_kwargs or {}
        self.spider_kwargs = spider_kwargs
        self.request_config = self.request_config or {}
        try:
            self.request_session = getattr(self, "request_session")
        except Exception as _:
            self.request_session = ClientSession()

        self.cancel_tasks = cancel_tasks
        self.is_async_start = is_async_start

        # set logger
        self.logger = get_logger(name=self.name)

        # customize middleware
        if isinstance(middleware, list):
            self.middleware = reduce(lambda x, y: x + y, middleware)
        else:
            self.middleware = middleware or Middleware()

        # async queue as a producer
        self.request_queue = asyncio.Queue()

        # semaphore, used for concurrency control
        self.sem = asyncio.Semaphore(self.concurrency)

    async def _process_async_callback(
        self, callback_result: AsyncGeneratorType, response: Response = None
    ):
        try:
            async for each_callback in callback_result:
                if isinstance(each_callback, AsyncGeneratorType):
                    await self._process_async_callback(each_callback)
                elif isinstance(each_callback, Request):
                    self.request_queue.put_nowait(
                        self.handle_request(request=each_callback)
                    )
                elif isinstance(each_callback, typing.Coroutine):
                    self.request_queue.put_nowait(
                        self.handle_callback(
                            aws_callback=each_callback, response=response
                        )
                    )
                elif isinstance(each_callback, Item):
                    # Process target item
                    await self.process_item(each_callback)
                else:
                    await self.process_callback_result(each_callback)
        except NothingMatchedError as e:
            error_info = f"<Field: {str(e).lower()}" + f", error url: {response.url}>"
            self.logger.error(error_info)
        except Exception as e:
            self.logger.error(e)

    async def _process_response(self, request: Request, response: Response):
        """
        Process Ruia's Response:
            count whether each request was successful or not, and call the handler function finally.
        """
        if response:
            if response.ok:
                # Process succeed response
                self.success_counts += 1
                await self.process_succeed_response(request, response)
            else:
                # Process failed response
                self.failed_counts += 1
                await self.process_failed_response(request, response)

    async def _run_request_middleware(self, request: Request):
        if self.middleware.request_middleware:
            for middleware in self.middleware.request_middleware:
                if callable(middleware):
                    try:
                        aws_middleware_func = middleware(self, request)
                        if isawaitable(aws_middleware_func):
                            await aws_middleware_func
                        else:
                            msg = f"<Middleware {middleware.__name__}: must be a coroutine function"
                            self.logger.error(msg)
                    except Exception as e:
                        msg = f"<Middleware {middleware.__name__}: {e}"
                        self.logger.error(msg)

    async def _run_response_middleware(self, request: Request, response: Response):
        if self.middleware.response_middleware:
            for middleware in self.middleware.response_middleware:
                if callable(middleware):
                    try:
                        aws_middleware_func = middleware(self, request, response)
                        if isawaitable(aws_middleware_func):
                            await aws_middleware_func
                        else:
                            msg = f"<Middleware {middleware.__name__}: must be a coroutine function"
                            self.logger.error(msg)
                    except Exception as e:
                        msg = f"<Middleware {middleware.__name__}: {e}"
                        self.logger.error(msg)

    async def _start(self, after_start=None, before_stop=None):
        """
        Crawler startup entry
        Args:
            after_start (_type_, optional): Hook function: executed before the crawler starts. Defaults to None.
            before_stop (_type_, optional): Hook function: executed before the crawler closes. Defaults to None.
        """
        self.logger.info("Spider started!")
        start_time = datetime.now()

        # Add signal
        for signal in (SIGINT, SIGTERM):
            try:
                self.loop.add_signal_handler(
                    signal, lambda: asyncio.ensure_future(self.stop(signal))
                )
            except NotImplementedError:
                self.logger.warning(
                    f"{self.name} tried to use loop.add_signal_handler "
                    "but it is not implemented on this platform."
                )
        # Run hook before spider start crawling
        await self._run_spider_hook(after_start)

        # Actually run crawling
        try:
            await self.start_master()
        finally:
            # Run hook after spider finished crawling
            await self._run_spider_hook(before_stop)
            if self.request_session is not None:
                await self.request_session.close()
            # Display logs about this crawl task
            end_time = datetime.now()
            self.logger.info(
                f"Total requests: {self.failed_counts + self.success_counts}"
            )

            if self.failed_counts:
                self.logger.info(f"Failed requests: {self.failed_counts}")
            self.logger.info(f"Time usage: {end_time - start_time}")
            self.logger.info("Spider finished!")

    @classmethod
    async def async_start(
        cls,
        middleware: typing.Union[typing.Iterable, Middleware] = None,
        loop=None,
        after_start=None,
        before_stop=None,
        cancel_tasks: bool = True,
        **spider_kwargs,
    ):
        """
        Start an async spider
        :param middleware: customize middleware or a list of middleware
        :param loop:
        :param after_start: hook
        :param before_stop: hook
        :param cancel_tasks: cancel async tasks
        :param spider_kwargs: Additional keyword args to initialize spider
        :return: An instance of :cls:`Spider`
        """
        loop = loop or asyncio.get_event_loop()
        spider_ins = cls(
            middleware=middleware,
            loop=loop,
            is_async_start=True,
            cancel_tasks=cancel_tasks,
            **spider_kwargs,
        )
        await spider_ins._start(after_start=after_start, before_stop=before_stop)

        return spider_ins

    @staticmethod
    async def cancel_all_tasks():
        """
        Cancel all tasks
        """
        tasks = []
        for task in async_all_tasks():
            if task is not async_current_task():
                tasks.append(task)
                task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)

    @classmethod
    def start(
        cls,
        middleware: typing.Union[typing.Iterable, Middleware] = None,
        loop=None,
        after_start=None,
        before_stop=None,
        close_event_loop=True,
        **spider_kwargs,
    ):
        """
        Start a spider
        :param after_start: hook
        :param before_stop: hook
        :param middleware: customize middleware or a list of middleware
        :param loop: event loop
        :param close_event_loop: bool
        :param spider_kwargs: Additional keyword args to initialize spider
        :return: An instance of :cls:`Spider`
        """
        loop = loop or asyncio.new_event_loop()
        spider_ins = cls(middleware=middleware, loop=loop, **spider_kwargs)

        # Actually start crawling
        spider_ins.loop.run_until_complete(
            spider_ins._start(after_start=after_start, before_stop=before_stop)
        )
        spider_ins.loop.run_until_complete(spider_ins.loop.shutdown_asyncgens())
        if close_event_loop:
            spider_ins.loop.close()

        return spider_ins

    async def handle_callback(self, aws_callback: typing.Coroutine, response):
        """
        Process coroutine callback function
        """
        callback_result = None

        try:
            callback_result = await aws_callback
        except NothingMatchedError as e:
            self.logger.error(f"<Item: {str(e).lower()}>")
        except Exception as e:
            self.logger.error(f"<Callback[{aws_callback.__name__}]: {e}")

        return callback_result, response

    async def handle_request(
        self, request: Request
    ) -> typing.Tuple[AsyncGeneratorType, Request, Response]:
        """
        Wrap request with middleware
        Args:
            request (Request): Ruia's Request

        Returns:
            typing.Tuple[AsyncGeneratorType, Request, Response]: Returns a result tuple after each request
        """
        callback_result, response = None, None

        try:
            await self._run_request_middleware(request)
            callback_result, response = await request.fetch_callback(self.sem)
            await self._run_response_middleware(request, response)
            await self._process_response(request=request, response=response)
        except NotImplementedParseError as e:
            self.logger.error(e)
        except NothingMatchedError as e:
            error_info = f"<Field: {str(e).lower()}" + f", error url: {request.url}>"
            self.logger.error(error_info)
        except Exception as e:
            self.logger.error(f"<Callback[{request.callback.__name__}]: {e}")

        return callback_result, request, response

    async def multiple_request(self, urls, is_gather=False, **kwargs):
        """
        For crawling multiple urls
        """
        if is_gather:
            resp_results = await asyncio.gather(
                *[self.handle_request(self.request(url=url, **kwargs)) for url in urls],
                return_exceptions=True,
            )
            for index, task_result in enumerate(resp_results):
                if not isinstance(task_result, RuntimeError) and task_result:
                    _, _, response = task_result
                    response.index = index
                    yield response
        else:
            for index, url in enumerate(urls):
                _, _, response = await self.handle_request(
                    self.request(url=url, **kwargs)
                )
                response.index = index
                yield response

    async def parse(self, response: Response):
        """
        Used for subclasses, directly parse the responses corresponding with start_urls
        :param response: Response
        :return:
        """
        raise NotImplementedParseError("<!!! parse function is expected !!!>")

    async def process_start_urls(self):
        """
        Process the start URLs
        :return: AN async iterator
        """
        for url in self.start_urls:
            yield self.request(url=url, callback=self.parse, metadata=self.metadata)

    def request(
        self,
        url: str,
        method: str = "GET",
        *,
        callback=None,
        encoding: typing.Optional[str] = None,
        headers: dict = None,
        metadata: dict = None,
        request_config: dict = None,
        request_session=None,
        **aiohttp_kwargs,
    ):
        """
        Init a Request class for crawling html
        Args:
            url (str):  Target url
            method (str, optional): HTTP method. Defaults to "GET".
            callback (_type_, optional): Callback func. Defaults to None.
            encoding (typing.Optional[str], optional): Html encoding. Defaults to None.
            headers (dict, optional): _description_. Request headers to None.
            metadata (dict, optional): _description_. Send the data to callback func to None.
            request_config (dict, optional): Manage the target request. Defaults to None.
            request_session (_type_, optional):  aiohttp.ClientSession. Defaults to None.

        Returns:
            _type_: Request
        """
        headers = headers or {}
        metadata = metadata or {}
        request_config = request_config or {}
        request_session = request_session or self.request_session

        headers.update(self.headers.copy())
        request_config.update(self.request_config.copy())
        aiohttp_kwargs.update(self.aiohttp_kwargs.copy())

        return Request(
            url=url,
            method=method,
            callback=callback,
            encoding=encoding,
            headers=headers,
            metadata=metadata,
            request_config=request_config,
            request_session=request_session,
            **aiohttp_kwargs,
        )

    async def start_master(self):
        """
        Actually start crawling
        """
        async for request_ins in self.process_start_urls():
            self.request_queue.put_nowait(self.handle_request(request_ins))
        workers = [
            asyncio.ensure_future(self.start_worker())
            for i in range(self.worker_numbers)
        ]
        for worker in workers:
            self.logger.info(f"Worker started: {id(worker)}")
        await self.request_queue.join()

        if not self.is_async_start:
            await self.stop(SIGINT)
        else:
            if self.cancel_tasks:
                await self.cancel_all_tasks()

    async def start_worker(self):
        """
        Start spider worker
        :return:
        """
        while True:
            request_item = await self.request_queue.get()
            self.worker_tasks.append(request_item)
            if self.request_queue.empty():
                results = await asyncio.gather(
                    *self.worker_tasks, return_exceptions=True
                )
                for task_result in results:
                    if not isinstance(task_result, RuntimeError) and task_result:
                        callback_result = task_result[0]
                        request: Request = task_result[1]
                        if isinstance(callback_result, AsyncGeneratorType):
                            await self._process_async_callback(
                                callback_result, task_result[2]
                            )
                        # Process Request's session
                        await request.close_request()

                self.worker_tasks = []
            self.request_queue.task_done()

    async def stop(self, _signal):
        """
        Finish all running tasks, cancel remaining tasks.
        :param _signal:
        :return:
        """
        self.logger.info(f"Stopping spider: {self.name}")
        await self.cancel_all_tasks()
        # self.loop.stop()
