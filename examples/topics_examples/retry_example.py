#!/usr/bin/env python
"""
 Created by howie.hu at 2018/11/21.
"""

from ruia import Request, Spider, Middleware

middleware = Middleware()


@middleware.request
async def print_on_request(request):
    request.headers = {
        'User-Agent': 'ruia ua'
    }


@middleware.response
async def print_on_response(request, response):
    print(request.headers)


async def retry_func(request):
    request.request_config['TIMEOUT'] = 10


class TestSpider(Spider):
    start_urls = ['http://www.httpbin.org/get']

    request_config = {
        'RETRIES': 3,
        'DELAY': 0,
        'TIMEOUT': 0.1,
        'RETRY_FUNC': retry_func
    }

    async def parse(self, response):
        pages = ['http://www.httpbin.org/get', 'http://www.httpbin.org/get']
        for index, page in enumerate(pages):
            yield Request(
                page,
                callback=self.parse_item,
                metadata={'index': index},
                request_config=self.request_config,
            )

    async def parse_item(self, response):
        item_data = response.html
        return item_data


if __name__ == '__main__':
    TestSpider.start(middleware=middleware)
