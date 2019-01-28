#!/usr/bin/env python

import asyncio

import pytest

from ruia import Request

sem = asyncio.Semaphore(3)


async def hello(response):
    return 'hello ruia'


async def retry_func(request):
    request.request_config['TIMEOUT'] = 10


request_config = {
    'RETRIES': 3,
    'DELAY': 1,
    'TIMEOUT': 0.1,
    'RETRY_FUNC': retry_func
}

headers = {
    "User-Agent": "Python3.6"
}

params = {
    "name": "ruia"
}
request = Request('http://www.httpbin.org/get',
                  method='GET',
                  metadata={'hello': 'ruia'},
                  res_type='json',
                  encoding='utf-8',
                  headers=headers,
                  request_config=request_config,
                  params=params,
                  callback=hello)


async def make_request(request=request):
    return await request.fetch_callback(sem)


callback_result, response = asyncio.get_event_loop().run_until_complete(make_request(request))


def test_request_config():
    assert str(request) == '<GET http://www.httpbin.org/get>'
    assert response.res_type == 'json'
    assert response.callback_result == 'hello ruia'
    assert response.html['args']['name'] == "ruia"
    assert response.html['headers']['User-Agent'] == "Python3.6"
