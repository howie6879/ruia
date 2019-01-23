#!/usr/bin/env python
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

    async def parse(self, response):
        SpiderDemo.result = response.html


async def after_start_func(spider_ins):
    assert type(spider_ins.result) == dict


async def before_stop_func(spider_ins):
    assert spider_ins.result['url'] == 'http://www.httpbin.org/get'


def test_spider():
    SpiderDemo.start(after_start=after_start_func, before_stop=before_stop_func)
    assert type(SpiderDemo.result) == dict
