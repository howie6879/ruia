#!/usr/bin/env python
import pytest

from ruia import Middleware

middleware = Middleware()


@middleware.request
async def print_on_request(request):
    request.headers = {
        'User-Agent': 'ruia ua'
    }


@middleware.response
async def print_on_response(request, response):
    print('print_on_response')


def test_middleware():
    assert middleware.request_middleware.pop().__name__ == 'print_on_request'
    assert middleware.response_middleware.pop().__name__ == 'print_on_response'
