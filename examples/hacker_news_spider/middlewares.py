#!/usr/bin/env python

from ruia import Middleware, Request

middleware = Middleware()


@middleware.request
async def print_on_request(spider_ins, request: Request):
    ua = "ruia user-agent"
    request.headers.update({"User-Agent": ua})


@middleware.request
async def request_proxy(spider_ins, request: Request):
    """request using proxy example"""
    # HTTP proxy
    # request.aiohttp_kwargs.update({"proxy": "http://0.0.0.0:1087"})

    # SOCKS5 proxy using aiohttp_socks
    # Check docs in https://pypi.org/project/aiohttp-socks/
    from aiohttp import ClientSession
    from aiohttp_socks import ProxyConnector
    # connector = ProxyConnector.from_url('socks5://username:password@127.0.0.1:1080')
    connector = ProxyConnector.from_url('socks5://127.0.0.1:9999')
    request.request_session = ClientSession(connector=connector)
    request.close_request_session = True
