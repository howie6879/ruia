#!/usr/bin/env python
"""
 Created by howie.hu at 2018/7/10.
"""
import aiohttp


class Request():
    """
    Request class for each request
    """
    name = 'Request'

    # Default config
    REQUEST_CONFIG = {
        'RETRIES': 3,
        'DELAY': 0,
        'TIMEOUT': 10
    }

    METHOD = ['GET', 'POST']

    def __init__(self):
        pass

    async def hi(self):
        async with aiohttp.ClientSession() as session:
            async with session.get('http://httpbin.org/get') as resp:
                print(resp.status)
                print(await resp.text())
