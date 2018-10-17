#!/usr/bin/env python
"""
 Created by howie.hu at 2018/9/21.
"""

from collections import deque
from functools import wraps


class Middleware:
    """
    Define a middleware to customize the crawler request or response
    eg: middleware = Middleware()
    """

    def __init__(self):
        # request middleware
        self.request_middleware = deque()
        # response middleware
        self.response_middleware = deque()

    def listener(self, uri, target, **kwargs):
        """
        Decorates to be called before a special request or response
        TODO: handling different urls for request/response
        eg: @middleware.listener('/post', 'request')
        """

        def register_middleware(middleware):
            if target == 'request':
                self.request_middleware.append(middleware)
            if target == 'response':
                self.response_middleware.appendleft(middleware)
            return middleware

        return register_middleware

    def request(self, *args, **kwargs):
        """
        Define a Decorate to be called before a request.
        eg: @middleware.request
        """
        middleware = args[0]

        @wraps(middleware)
        def register_middleware(*args, **kwargs):
            self.request_middleware.append(middleware)
            return middleware

        return register_middleware()

    def response(self, *args, **kwargs):
        """
        Define a Decorate to be called after a response.
        eg: @middleware.response
        """
        middleware = args[0]

        @wraps(middleware)
        def register_middleware(*args, **kwargs):
            self.response_middleware.appendleft(middleware)
            return middleware

        return register_middleware()

    def __add__(self, other):
        new_middleware = Middleware()
        # asc
        new_middleware.request_middleware.extend(self.request_middleware)
        new_middleware.request_middleware.extend(other.request_middleware)
        # desc
        new_middleware.response_middleware.extend(other.response_middleware)
        new_middleware.response_middleware.extend(self.response_middleware)
        return new_middleware
