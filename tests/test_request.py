#!/usr/bin/env python

import asyncio

from ruia import Request

sem = asyncio.Semaphore(3)


async def hello(response):
    yield hello2(response)


async def hello2(response):
    return 'hello ruia'


async def retry_func(request):
    request.request_config['TIMEOUT'] = 10


headers = {
    "User-Agent": "Python3.6"
}

params = {
    "name": "ruia"
}


async def timeout_request(sem):
    request_config = {
        'RETRIES': 1,
        'DELAY': 1,
        'TIMEOUT': 0.1,
    }
    request = Request('http://www.httpbin.org/get',
                      method='GET',
                      metadata={'hello': 'ruia'},
                      encoding='utf-8',
                      headers=headers,
                      request_config=request_config,
                      params=params,
                      callback=hello)
    return await request.fetch_callback(sem)


async def make_request(sem, callback=None):
    request_config = {
        'RETRIES': 3,
        'DELAY': 1,
        'TIMEOUT': 0.1,
        'RETRY_FUNC': retry_func
    }
    request = Request('http://www.httpbin.org/get',
                      method='GET',
                      metadata={'hello': 'ruia'},
                      headers=headers,
                      request_config=request_config,
                      params=params,
                      callback=callback)
    return await request.fetch_callback(sem)


def test_request_config():
    asyncio.get_event_loop().run_until_complete(make_request(sem=sem, callback=hello))
    callback_result, response = asyncio.get_event_loop().run_until_complete(make_request(sem=sem, callback=hello2))
    assert response.callback_result == 'hello ruia'
    json_result = asyncio.get_event_loop().run_until_complete(response.json())
    assert json_result['args']['name'] == "ruia"
    assert json_result['headers']['User-Agent'] == "Python3.6"


def test_timeout_request():
    callback_result, response = asyncio.get_event_loop().run_until_complete(timeout_request(sem=sem))
    assert response.url == 'http://www.httpbin.org/get'
