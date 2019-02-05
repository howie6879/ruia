#!/usr/bin/env python
import pytest

from ruia import Middleware

middleware = Middleware()

res_type_middleware = Middleware()


@middleware.request
async def print_on_request(request):
    request.headers = {
        'User-Agent': 'ruia ua'
    }


@middleware.response
async def print_on_response(request, response):
    assert type(response.html) == dict


@res_type_middleware.request
async def print_on_request(request):
    request.res_type = 'json'


@res_type_middleware.response
async def print_on_response(request, response):
    assert type(response.html) == dict


all_middleware = middleware + res_type_middleware


@all_middleware.request
async def print_on_request(request):
    request.res_type = 'json'


@all_middleware.response
async def print_on_response(request, response):
    assert type(response.html) == dict


def test_add_middleware():
    assert len(all_middleware.request_middleware) == 3
    assert len(all_middleware.response_middleware) == 3
    assert all_middleware.request_middleware.pop().__name__ == 'print_on_request'
    assert all_middleware.response_middleware.pop().__name__ == 'print_on_response'
    assert len(all_middleware.request_middleware) == 2
    assert len(all_middleware.response_middleware) == 2


def test_request_middleware():
    assert len(middleware.request_middleware) == 1
    assert middleware.request_middleware.pop().__name__ == 'print_on_request'


def test_response_middleware():
    assert middleware.response_middleware.pop().__name__ == 'print_on_response'
