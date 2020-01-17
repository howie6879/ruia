#!/usr/bin/env python

from ruia import Middleware

middleware01 = Middleware()

middleware02 = Middleware()


@middleware01.request
async def print_on_request01(spider_ins, request):
    request.headers = {"User-Agent": "ruia ua"}


@middleware01.response
async def print_on_response01(spider_ins, request, response):
    assert isinstance(response.html, str)


@middleware02.request
async def print_on_request02(spider_ins, request):
    pass


@middleware02.response
async def print_on_response02(spider_ins, request, response):
    pass


all_middleware = middleware01 + middleware02


@all_middleware.request
async def print_on_request(spider_ins, request):
    pass


@all_middleware.response
async def print_on_response(spider_ins, request, response):
    pass


def test_add_middleware():
    assert len(all_middleware.request_middleware) == 3
    assert len(all_middleware.response_middleware) == 3
    assert all_middleware.request_middleware.pop().__name__ == "print_on_request"
    assert all_middleware.response_middleware.pop().__name__ == "print_on_response01"
    assert len(all_middleware.request_middleware) == 2
    assert len(all_middleware.response_middleware) == 2


def test_request_middleware():
    assert len(middleware01.request_middleware) == 1
    assert middleware01.request_middleware.pop().__name__ == "print_on_request01"


def test_response_middleware():
    assert middleware01.response_middleware.pop().__name__ == "print_on_response01"
