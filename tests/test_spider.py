#!/usr/bin/env python

import asyncio
import os

from ruia import Item, Middleware, Response, Request, Spider, TextField
from ruia.exceptions import SpiderHookError

html_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "data", "for_spider_testing.html"
)
with open(html_path, mode="r", encoding="utf-8") as file:
    HTML = file.read()

middleware = Middleware()


async def retry_func(request):
    request.request_config["TIMEOUT"] = 10


@middleware.request
async def print_on_request(spider_ins, request):
    request.headers = {"User-Agent": "ruia ua"}


@middleware.response
async def print_on_response(spider_ins, request, response):
    assert isinstance(response.html, str)
    assert request.headers == {"User-Agent": "ruia ua"}


class ItemDemo(Item):
    title = TextField(xpath_select="/html/head/title")


class SpiderDemo(Spider):
    start_urls = ["https://httpbin.org/get?p=0"]
    request_config = {"RETRIES": 3, "DELAY": 0, "TIMEOUT": 20}
    headers = {"User-Agent": "Ruia Spider"}
    aiohttp_kwargs = {}

    call_nums = 0

    async def parse(self, response):
        yield Request(
            url=response.url,
            callback=self.parse_item,
            headers=self.headers,
            request_config=self.request_config,
            **self.aiohttp_kwargs,
        )

    async def parse_item(self, response):
        pages = [f"https://httpbin.org/get?p={i}" for i in range(1, 2)]
        async for resp in self.multiple_request(pages):
            yield self.parse_next(response=resp, any_param="hello")

    async def parse_next(self, response, any_param):
        assert any_param == "hello"
        yield self.request(
            url="https://httpbin.org/get?p=2",
            metadata={"any_param": any_param},
            callback=self.parse_details,
        )

    async def parse_details(self, response):
        item = await ItemDemo.get_item(html=HTML)
        yield item

    async def process_item(self, item: ItemDemo):
        assert item.title == "for_spider_testing"
        await self.count_nums()

    async def count_nums(self):
        SpiderDemo.call_nums += 1


def test_spider_with_middleware():
    loop = asyncio.new_event_loop()
    SpiderDemo.start(loop=loop, middleware=middleware)
    assert SpiderDemo.call_nums == 1


def test_spider_with_error_middleware():
    error_middleware = Middleware()

    @error_middleware.request
    def error_request(spider_ins, request, response):
        pass

    @error_middleware.response
    async def error_response(spider_ins, request, response):
        raise TypeError("error")

    class SpiderDemo(Spider):
        start_urls = ["https://httpbin.org/get?p=0"]

        async def parse(self, response):
            pass

    SpiderDemo.start(middleware=error_middleware)


def test_spider_hook():
    async def after_start_func(spider_ins):
        print("after_start_func")
        spider_ins.result["after_start"] = True
        assert isinstance(spider_ins.result, dict)

    async def before_stop_func(spider_ins):
        print("before_stop_func")
        spider_ins.result["before_stop"] = True

    class SpiderHook(Spider):
        start_urls = ["https://httpbin.org/get?p=0", "https://httpbin.org/404"]
        request_config = {"RETRIES": 1, "DELAY": 0, "TIMEOUT": 10}

        result = {
            "after_start": False,
            "before_stop": False,
            "process_succeed_response": False,
            "process_failed_response": False,
            "process_item": False,
        }

        async def parse(self, response):
            item = await ItemDemo.get_item(html=HTML)
            yield item

        async def process_item(self, item):
            self.result["process_item"] = True

        async def process_succeed_response(self, request, response):
            # Hook for response
            self.result["process_succeed_response"] = True

        async def process_failed_response(self, request, response):
            # Hook for response
            self.result["process_failed_response"] = True

    # Test middleware & hook
    loop = asyncio.new_event_loop()
    SpiderHook.start(
        loop=loop, after_start=after_start_func, before_stop=before_stop_func
    )

    assert SpiderHook.result["after_start"] == True
    assert SpiderHook.result["before_stop"] == True
    assert SpiderHook.result["process_succeed_response"] == True
    assert SpiderHook.result["process_failed_response"] == True
    assert SpiderHook.result["process_item"] == True


def test_spider_hook_error():
    class SpiderDemo(Spider):
        start_urls = ["https://httpbin.org/get?p=0"]

        async def parse(self, response):
            pass

    async def before_stop_func(spider_ins):
        raise TypeError("error")

    loop = asyncio.new_event_loop()
    try:
        SpiderDemo.start(loop=loop, before_stop=before_stop_func)
    except Exception as e:
        assert isinstance(e, SpiderHookError)


def test_invalid_callback_result():
    class SpiderDemo(Spider):
        start_urls = ["https://httpbin.org/get?p=0"]
        result = {"process_callback_result": False}

        async def parse(self, response):
            yield {}

    async def process_dict_callback_result(spider_ins, callback_result):
        spider_ins.result["process_callback_result"] = True

    class CustomCallbackResultType:
        @classmethod
        def init_spider(cls, spider):
            spider.callback_result_map = spider.callback_result_map or {}
            setattr(
                spider, "process_dict_callback_result", process_dict_callback_result
            )
            spider.callback_result_map.update({"dict": "process_dict_callback_result"})

    CustomCallbackResultType.init_spider(SpiderDemo)

    loop = asyncio.new_event_loop()
    SpiderDemo.start(loop=loop)
    assert SpiderDemo.result["process_callback_result"] == True


def test_spider_multiple_request_sync():
    result = list()

    class MultipleRequestSpider(Spider):
        start_urls = ["https://httpbin.org"]
        concurrency = 3

        async def parse(self, response: Response):
            urls = [f"https://httpbin.org/get?p={page}" for page in range(1, 2)]
            async for response in self.multiple_request(urls, is_gather=True):
                yield self.parse_next(response=response)

        async def parse_next(self, response):
            json_result = await response.json()
            page = json_result["args"]["p"]
            result.append(int(page))

    MultipleRequestSpider.start()
    assert result == [1]


def test_no_start_url_spider():
    try:

        class NoStartUrlSpider(Spider):
            pass

        NoStartUrlSpider.start()
    except Exception as e:
        assert isinstance(e, ValueError)


def test_callback_error():
    class NoParseSpider(Spider):
        start_urls = ["https://httpbin.org/get"]

    NoParseSpider.start()

    class CallbackError(Spider):
        start_urls = ["https://httpbin.org/get"]

        async def parse(self, response):
            raise ValueError("error")

    CallbackError.start()


def test_coroutine_callback_error():
    class CoroutineItemErrorSpider(Spider):
        start_urls = ["https://httpbin.org/get"]

        async def parse(self, response):
            pages = ["https://httpbin.org/get?p=1"]
            async for resp in self.multiple_request(pages):
                yield self.parse_item(response=resp)

        async def parse_item(self, response):
            await ItemDemo.get_item(html=response.html)

    CoroutineItemErrorSpider.start()

    class CoroutineErrorSpider(Spider):
        start_urls = ["https://httpbin.org/get"]

        async def parse(self, response):
            pages = ["https://httpbin.org/get?p=1"]
            async for resp in self.multiple_request(pages):
                yield self.parse_item(response=resp)

        async def parse_item(self, response):
            raise ValueError("error")

    CoroutineErrorSpider.start()


def test_nothing_matched_spider():
    class NothingMatchedErrorSpider(Spider):
        start_urls = ["https://httpbin.org/get"]

        async def parse(self, response):
            await ItemDemo.get_item(html=response.html)

    NothingMatchedErrorSpider.start()


def test_multiple_spider():
    class MultipleSpider(Spider):
        count = 0
        start_urls = ["https://httpbin.org/get?p=0"]

        async def parse(self, response):
            MultipleSpider.count += 1

    async def multiple_spider(loop):
        await MultipleSpider.async_start(loop=loop, middleware=[middleware])
        await MultipleSpider.async_start(loop=loop, middleware=middleware)
        return MultipleSpider

    loop = asyncio.new_event_loop()
    spider_ins = loop.run_until_complete(multiple_spider(loop=loop))
    assert spider_ins.count == 2
