#!/usr/bin/env python
"""
 Created by howie.hu at 2019/1/28.
"""
import asyncio

from lxml import etree
from aiohttp.cookiejar import SimpleCookie

import pytest

from ruia import Request


async def hello(response):
    return 'hello ruia'


sem = asyncio.Semaphore(3)
params = {
    "name": "ruia"
}
request = Request('http://www.httpbin.org/get',
                  method='GET',
                  metadata={'hello': 'ruia'},
                  res_type='text',
                  params=params,
                  callback=hello)
_, response = asyncio.get_event_loop().run_until_complete(request.fetch_callback(sem))


def test_response():
    url = response.url
    method = response.method
    metadata = response.metadata
    res_type = response.res_type
    html = response.html
    cookies = response.cookies
    history = response.history
    headers = response.headers
    status = response.status
    html_etree = response.html_etree

    assert url == 'http://www.httpbin.org/get'
    assert method == 'GET'
    assert metadata == {'hello': 'ruia'}
    assert res_type == 'text'
    assert type(html) == str
    assert type(cookies) == SimpleCookie
    assert history == ()
    assert headers['Content-Type'] == 'application/json'
    assert status == 200
    assert type(html_etree) == etree._Element

    assert str(response) == '<Response url[GET]: http://www.httpbin.org/get status:200 html_type:text>'


def test_callback():
    assert response.callback_result == 'hello ruia'
    response.callback_result = 'ruia'
    assert response.callback_result == 'ruia'


def test_index():
    assert response.index == None
    response.index = 'ruia'
    assert response.index == 'ruia'
