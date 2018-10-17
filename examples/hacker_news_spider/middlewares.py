#!/usr/bin/env python
"""
 Created by howie.hu at 2018/9/23.
"""

from ruia import Middleware

middleware = Middleware()


@middleware.request
async def print_on_request(request):
    ua = 'ruia user-agent'
    request.headers.update({'User-Agent': ua})
    # request.kwargs.update({"proxy": "http://0.0.0.0:8118"})
