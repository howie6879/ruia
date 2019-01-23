#!/usr/bin/env python

from ruia import Request, Spider, Middleware


class TestSpider(Spider):
    start_urls = ['http://www.httpbin.org/get']

    async def parse(self, response):
        pages = ['http://www.httpbin.org/get', 'http://www.httpbin.org/get']
        for index, page in enumerate(pages):
            yield Request(
                page,
                callback=self.parse_item,
                metadata={'index': index}
            )

    async def parse_item(self, response):
        item_data = response.html
        return item_data


middleware = Middleware()
res_type_middleware = Middleware()


@middleware.request
async def print_on_request(request):
    request.headers = {
        'User-Agent': 'ruia ua'
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
