#!/usr/bin/env python
import asyncio

import pytest

from ruia import Middleware, Spider, Item, TextField, AttrField

middleware = Middleware()


class SpiderDemo(Spider):
    start_urls = ['http://www.httpbin.org/get']
    request_config = {
        'RETRIES': 3,
        'DELAY': 0,
        'TIMEOUT': 20
    }
    concurrency = 1
    res_type = 'json'
    result = {
        'after_start': False,
        'before_stop': False,
    }
    call_nums = 0

    async def parse(self, response):
        SpiderDemo.call_nums += 1


async def after_start_func(spider_ins):
    print("after_start_func")
    spider_ins.result['after_start'] = True
    assert type(spider_ins.result) == dict


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
    assert type(response.html) == dict
    assert request.headers == {
        'User-Agent': 'ruia ua'
    }


class HackerNewsItem(Item):
    target_item = TextField(css_select='tr.athing')
    title = TextField(css_select='a.storylink')
    url = AttrField(css_select='a.storylink', attr='href')

    async def clean_title(self, value):
        return value.strip()


class HackerNewsSpider(Spider):
    start_urls = ['https://news.ycombinator.com/news?p=1', 'https://news.ycombinator.com/news?p=2']
    concurrency = 10

    async def parse(self, response):
        async for item in HackerNewsItem.get_items(html=response.html):
            yield item

    async def process_item(self, item: HackerNewsItem):
        assert type(item) == HackerNewsItem
        yield self.request(url='http://www.httpbin.org/get', res_type='json', callback=self.parse_httpbin_item)

    async def parse_httpbin_item(self, response):
        assert type(response.html) == dict


class NoStartUrlSpider(Spider):
    pass


def test_spider():
    loop = asyncio.new_event_loop()
    SpiderDemo.start(loop=loop, middleware=middleware, after_start=after_start_func, before_stop=before_stop_func)
    assert type(SpiderDemo.result) == dict
    assert SpiderDemo.result['after_start'] == True
    assert SpiderDemo.result['before_stop'] == True

    HackerNewsSpider.start()


def test_no_start_url_spider():
    try:
        NoStartUrlSpider.start()
    except Exception as e:
        assert type(e) == ValueError


async def multiple_spider(loop):
    await SpiderDemo.async_start(loop=loop, after_start=after_start_func, before_stop=before_stop_func)
    await SpiderDemo.async_start(loop=loop, after_start=after_start_func, before_stop=before_stop_func)
    return SpiderDemo


def test_multiple_spider():
    loop = asyncio.new_event_loop()
    SpiderDemo = loop.run_until_complete(multiple_spider(loop=loop))
    assert SpiderDemo.call_nums == 3
