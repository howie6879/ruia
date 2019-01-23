#!/usr/bin/env python
import asyncio

import pytest

from ruia import Spider


class SpiderDemo(Spider):
    start_urls = ['http://www.httpbin.org/get']
    request_config = {
        'RETRIES': 3,
        'DELAY': 0,
        'TIMEOUT': 20
    }
    concurrency = 1
    res_type = 'json'
    result = {}
    call_nums = 0

    async def parse(self, response):
        SpiderDemo.result = response.html
        SpiderDemo.call_nums += 1


async def after_start_func(spider_ins):
    print("after_start_func")
    assert type(spider_ins.result) == dict


async def before_stop_func(spider_ins):
    print("before_stop_func")
    assert spider_ins.result['url'] == 'http://www.httpbin.org/get'


async def multiple_spider():
    await SpiderDemo.async_start(after_start=after_start_func, before_stop=before_stop_func)
    await SpiderDemo.async_start(after_start=after_start_func, before_stop=before_stop_func)
    await SpiderDemo.async_start(after_start=after_start_func, before_stop=before_stop_func)


def test_multiple_spider():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(multiple_spider())
    assert SpiderDemo.call_nums == 3


def test_spider():
    SpiderDemo.start(after_start=after_start_func, before_stop=before_stop_func)
    assert type(SpiderDemo.result) == dict
