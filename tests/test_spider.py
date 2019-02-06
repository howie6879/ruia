#!/usr/bin/env python
import asyncio

import pytest
from ruia import AttrField, Item, Middleware, Request, Spider, TextField, Response

middleware = Middleware()


async def after_start_func(spider_ins):
    print("after_start_func")
    spider_ins.result['after_start'] = True
    assert isinstance(spider_ins.result, dict)


async def before_stop_func(spider_ins):
    print("before_stop_func")
    spider_ins.result['before_stop'] = True


@middleware.request
async def print_on_request(request):
    request.headers = {
        'User-Agent': 'ruia ua'
    }


@middleware.response
async def print_on_response(request, response):
    assert isinstance(response.html, dict)
    assert request.headers == {
        'User-Agent': 'ruia ua'
    }


class SpiderDemo(Spider):
    start_urls = ['http://www.httpbin.org/get']
    request_config = {
        'RETRIES': 3,
        'DELAY': 0,
        'TIMEOUT': 20
    }
    headers = {
        "User-Agent": "Python3.6"
    }
    concurrency = 1
    res_type = 'json'
    result = {
        'after_start': False,
        'before_stop': False,
    }
    call_nums = 0
    kwargs = {}

    async def parse(self, response):
        yield Request(
            url=response.url,
            callback=self.parse_item,
            headers=self.headers,
            request_config=self.request_config,
            **self.kwargs
        )

    async def parse_item(self, response):
        pages = [{'url': f'http://www.httpbin.org/get?p={i}'} for i in range(1, 2)]
        async for resp in self.multiple_request(pages):
            yield self.parse_next(resp, any_param='hello')

    async def parse_next(self, response, any_param):
        SpiderDemo.call_nums += 1


class HackerNewsItem(Item):
    target_item = TextField(css_select='tr.athing')
    title = TextField(css_select='a.storylink')
    url = AttrField(css_select='a.storylink', attr='href')

    async def clean_title(self, value):
        return value.strip()


class HackerNewsSpider(Spider):
    name = 'test_spider'
    start_urls = ['https://news.ycombinator.com/news?p=1']
    concurrency = 10

    async def parse(self, response):
        async for item in HackerNewsItem.get_items(html=response.html):
            yield item

    async def process_item(self, item: HackerNewsItem):
        assert isinstance(item, HackerNewsItem)
        pages = [{'url': f'http://www.httpbin.org/get?p={i}'} for i in range(1, 2)]
        async for resp in self.multiple_request(pages, is_gather=True):
            yield self.parse_httpbin_item(resp)

    async def parse_httpbin_item(self, response):
        assert isinstance(response.html, str)


class NoStartUrlSpider(Spider):
    pass


class NoParseSpider(Spider):
    start_urls = ['http://www.httpbin.org/get']


class InvalidParseTypeSpider(Spider):
    start_urls = ['http://www.httpbin.org/get']

    async def parse(self, response):
        yield 2


def test_spider():
    loop = asyncio.new_event_loop()
    SpiderDemo.start(loop=loop, middleware=middleware, after_start=after_start_func, before_stop=before_stop_func)
    assert isinstance(SpiderDemo.result, dict)
    assert SpiderDemo.result['after_start'] == True
    assert SpiderDemo.result['before_stop'] == True

    HackerNewsSpider.start()


def test_no_start_url_spider():
    try:
        NoStartUrlSpider.start()
    except Exception as e:
        assert isinstance(e, ValueError)


def test_invalid_parse_type_spider():
    InvalidParseTypeSpider.start()
    NoParseSpider.start()


async def multiple_spider(loop):
    await SpiderDemo.async_start(loop=loop, after_start=after_start_func, before_stop=before_stop_func)
    await SpiderDemo.async_start(loop=loop, after_start=after_start_func, before_stop=before_stop_func)
    return SpiderDemo


def test_multiple_spider():
    loop = asyncio.new_event_loop()
    SpiderDemo = loop.run_until_complete(multiple_spider(loop=loop))
    assert SpiderDemo.call_nums == 3


def test_multiple_request_sync():
    class MultipleRequestSpider(Spider):
        start_urls = ['https://httpbin.org']
        concurrency = 3

        async def parse(self, response: Response):
            urls = [f'https://httpbin.org/get?p={page}' for page in range(2)]
            async for response in self.multiple_request(urls, is_gather=False):
                # TODO: should use response.json instead
                assert isinstance(response.html, str)

    MultipleRequestSpider.start()


def test_multiple_request_async():
    class MultipleRequestSpider(Spider):
        start_urls = ['https://httpbin.org']
        concurrency = 3

        async def parse(self, response: Response):
            urls = [f'https://httpbin.org/get?p={page}' for page in range(4)]
            async for response in self.multiple_request(urls, is_gather=True):
                # TODO: should use response.json instead
                assert isinstance(response.html, str)

    MultipleRequestSpider.start()
