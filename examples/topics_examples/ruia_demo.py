#!/usr/bin/env python
import asyncio

from ruia import AttrField, Item, Middleware, Request, Spider, TextField, Response
sem = asyncio.Semaphore(3)


async def hello(response):
    yield hello2(response)

async def hello2(response):
    return 'hi ruia'

async def retry_func(request):
    request.request_config['TIMEOUT'] = 10


headers = {
    "User-Agent": "Python3.6"
}

params = {
    "name": "ruia"
}


async def make_request(sem):
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
                      callback=hello)
    return await request.fetch_callback(sem)


try:
    callback_result, response = asyncio.get_event_loop().run_until_complete(make_request(sem=sem))
    print(response.callback_result)
except Exception as e:
    print(e)