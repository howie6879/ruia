#!/usr/bin/env python
"""
 Created by howie.hu at 2018/9/22.
"""

from aspider import Request, Spider, Middleware


class TestSpider(Spider):
    start_urls = ['http://www.httpbin.org/get']

    async def parse(self, res):
        pages = ['http://www.httpbin.org/get', 'http://www.httpbin.org/get']
        for index, page in enumerate(pages):
            yield Request(
                page,
                callback=self.parse_item,
                metadata={'index': index},
                request_config=self.request_config,
            )

    async def parse_item(self, res):
        item_data = res.html
        return item_data


middleware = Middleware()
res_type_middleware = Middleware()


@middleware.request
async def print_on_request(request):
    request.headers = {
        'User-Agent': 'aspider ua'
    }


@middleware.response
async def print_on_response(request, response):
    assert type(response.html) == dict


@res_type_middleware.request
async def print_on_request(request):
    request.res_type = 'json'


@res_type_middleware.response
async def print_on_response(request, response):
    assert type(response.html) == dict


if __name__ == '__main__':
    TestSpider.start(middleware=[middleware, res_type_middleware])
