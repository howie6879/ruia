#!/usr/bin/env python
"""
 Created by howie.hu at 2018/7/10.
"""
import asyncio

from aspider import Request

def test_request_params():
    params = {
        "name": "aspider"
    }
    request = Request('http://www.httpbin.org/get', method='GET', res_type='json', params=params)
    result = asyncio.get_event_loop().run_until_complete(request.fetch())
    assert result.html['args']['name'] == "aspider"

def test_request_ua():
    headers = {
        "User-Agent": "Python3.5"
    }
    request = Request('http://www.httpbin.org/get', method='GET', res_type='json', headers=headers)
    result = asyncio.get_event_loop().run_until_complete(request.fetch())
    assert result.html['headers']['User-Agent'] == "Python3.5"

