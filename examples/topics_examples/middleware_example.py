#!/usr/bin/env python

from ruia import Spider, Middleware


class TestSpider(Spider):
    start_urls = ['http://www.httpbin.org/get']
    concurrency = 10

    async def parse(self, response):
        pages = [f'http://www.httpbin.org/get?p={i}' for i in range(1, 3)]
        async for resp in self.multiple_request(urls=pages):
            yield self.parse_next(resp, any_param='hello')

    async def parse_next(self, response, any_param):
        yield self.request(
            url=response.url,
            callback=self.parse_item
        )

    async def parse_item(self, response):
        print(response.html)


middleware = Middleware()
res_type_middleware = Middleware()


@middleware.request
async def print_on_request01(request):
    request.headers = {
        'User-Agent': 'ruia ua'
    }


@middleware.response
async def print_on_response01(request, response):
    assert isinstance(response.html, dict)


@res_type_middleware.request
async def print_on_request02(request):
    request.res_type = 'json'


@res_type_middleware.response
async def print_on_response02(request, response):
    assert isinstance(response.html, dict)


if __name__ == '__main__':
    TestSpider.start(middleware=[middleware, res_type_middleware])
