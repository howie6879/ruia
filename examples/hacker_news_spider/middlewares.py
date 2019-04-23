#!/usr/bin/env python

from ruia import Middleware

middleware = Middleware()


@middleware.request
async def print_on_request(spider_ins, request):
    ua = 'ruia user-agent'
    request.headers.update({'User-Agent': ua})
    # request.kwargs.update({"proxy": "http://0.0.0.0:8118"})
