#!/usr/bin/env python

from ruia import Spider


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
        pages = ['http://www.httpbin.org/get?p=1', 'http://www.httpbin.org/get?p=2']
        async for resp in self.multiple_request(pages):
            yield self.parse_item(response=resp)

    async def parse_item(self, response):
        json_data = await response.json()
        return json_data


if __name__ == '__main__':
    TestSpider.start()
