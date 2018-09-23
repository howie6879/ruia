#!/usr/bin/env python
"""
 Created by howie.hu at 2018/9/23.
"""

from aspider import Middleware

middleware = Middleware()


@middleware.request
async def print_on_request(request):
    ua = 'aspider user-agent'
    request.headers.update({'User-Agent': ua})
