#!/usr/bin/env python
"""
 Created by howie.hu at 2018/7/26.
"""
from aspider import Request, Spider


class Hello(Spider):
    start_urls = ['http://www.httpbin.org/get?a=1']
    headers = {
        "User-Agent": "Python3.5"
    }
    name = 'spider-test'
    concurrency = 100

    async def parse(self, res):
        for i in range(1):
            yield Request('http://www.httpbin.org/get', callback=self.parse_details, metadata={'2': i})

    async def parse_details(self, res):
        pass


# Hello.start()
# Hello.start()
# Hello.start()


