#!/usr/bin/env python

from ruia import Spider, Middleware


class TestSpider(Spider):
    start_urls = ['http://www.httpbin.org/get']

    async def parse(self, response):
        pages = [{'url': f'http://www.httpbin.org/get?p={i}'} for i in range(1, 9)]
        async for resp in self.multiple_request(pages):
            yield self.parse_next(resp, any_param='hello')

    async def parse_next(self, response, any_param):
        yield self.request(
            url=response.url,
            callback=self.parse_item
        )

    async def parse_item(self, response):
        item_data = response.html
        # print(item_data)


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
