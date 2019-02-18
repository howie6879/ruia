#!/usr/bin/env python

from ruia import Spider


async def after_start_func(spider_ins):
    print("after_start_func")
    spider_ins.result['after_start'] = True
    assert isinstance(spider_ins.result, dict)


async def before_stop_func(spider_ins):
    print("before_stop_func")
    spider_ins.result['before_stop'] = True


class HookDemoSpider(Spider):
    start_urls = ['https://httpbin.org/get?p=0', 'https://httpbin.org/404']
    request_config = {
        'RETRIES': 1,
        'DELAY': 0,
        'TIMEOUT': 10,

    }

    result = {
        'after_start': False,
        'before_stop': False,
        'process_succeed_response': False,
        'process_failed_response': False,
        'process_callback_result': False
    }

    async def parse(self, response):
        if response.ok:
            yield await response.json()

    async def process_callback_result(self, callback_result):
        if isinstance(callback_result, dict):
            print(callback_result)
            self.result['process_callback_result'] = True

    async def process_succeed_response(self, request, response):
        # Hook for response
        self.result['process_succeed_response'] = True

    async def process_failed_response(self, request, response):
        # Hook for response
        self.result['process_failed_response'] = True


if __name__ == '__main__':
    HookDemoSpider.start(after_start=after_start_func, before_stop=before_stop_func)

    assert HookDemoSpider.result['after_start'] == True
    assert HookDemoSpider.result['before_stop'] == True
    assert HookDemoSpider.result['process_succeed_response'] == True
    assert HookDemoSpider.result['process_failed_response'] == True
    assert HookDemoSpider.result['process_callback_result'] == True
