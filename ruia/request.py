#!/usr/bin/env python

import asyncio
import weakref

import aiohttp
import async_timeout

from inspect import iscoroutinefunction
from types import AsyncGeneratorType
from typing import Coroutine, Optional, Tuple

from asyncio.locks import Semaphore

try:
    import uvloop

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass

from ruia.exceptions import InvalidRequestMethod
from ruia.response import Response
from ruia.utils import get_logger


class Request(object):
    """
    Request class for each request
    """
    name = 'Request'

    # Default config
    REQUEST_CONFIG = {
        'RETRIES': 3,
        'DELAY': 0,
        'TIMEOUT': 10,
        'RETRY_FUNC': Coroutine,
        'VALID': Coroutine
    }

    METHOD = ['GET', 'POST']

    def __init__(self,
                 url: str,
                 method: str = 'GET',
                 *,
                 callback=None,
                 encoding: Optional[str] = None,
                 headers: dict = None,
                 metadata: dict = None,
                 request_config: dict = None,
                 request_session=None,
                 **kwargs):
        """
        Initialization parameters
        """
        self.url = url
        self.method = method.upper()
        if self.method not in self.METHOD:
            raise InvalidRequestMethod(
                f'{self.method} method is not supported'
            )

        self.callback = callback
        self.encoding = encoding
        self.headers = headers or {}
        self.metadata = metadata or {}
        self.request_session = request_session
        self.request_config = self.REQUEST_CONFIG if request_config is None else request_config
        self.ssl = kwargs.pop('ssl', False)
        self.kwargs = kwargs

        self.close_request_session = False
        self.logger = get_logger(name=self.name)
        self.retry_times = self.request_config.get('RETRIES', 3)

    @property
    def current_request_session(self):
        if self.request_session is None:
            self.request_session = aiohttp.ClientSession()
            self.close_request_session = True
        return self.request_session

    async def fetch(self) -> Response:
        """Fetch all the information by using aiohttp"""
        if self.request_config.get('DELAY', 0) > 0:
            await asyncio.sleep(self.request_config['DELAY'])

        timeout = self.request_config.get('TIMEOUT', 10)
        try:
            async with async_timeout.timeout(timeout):
                resp = await self._make_request()
            try:
                resp_data = await resp.text(encoding=self.encoding)
            except UnicodeDecodeError:
                resp_data = await resp.read()

            response = Response(
                url=self.url,
                method=self.method,
                encoding=resp.get_encoding(),
                html=resp_data,
                metadata=self.metadata,
                cookies=resp.cookies,
                headers=resp.headers,
                history=resp.history,
                status=resp.status,
                aws_json=resp.json,
                aws_text=resp.text,
                aws_read=resp.read)
            # Retry middleware
            aws_valid_response = self.request_config.get('VALID')
            if aws_valid_response and iscoroutinefunction(aws_valid_response):
                response = await aws_valid_response(response)
            if response.ok:
                return response
            else:
                return await self._retry(error_msg='request url failed!')
        except asyncio.TimeoutError:
            return await self._retry(error_msg='timeout')
        except Exception as e:
            return await self._retry(error_msg=e)
        finally:
            # Close client session
            await self._close_request_session()

    async def fetch_callback(
            self, sem: Semaphore) -> Tuple[AsyncGeneratorType, Response]:
        try:
            async with sem:
                response = await self.fetch()
        except Exception as e:
            response = None
            self.logger.error(f"<Error: {self.url} {e}>")

        if self.callback is not None:
            if iscoroutinefunction(self.callback):
                callback_result = await self.callback(response)
                response.callback_result = callback_result
            else:
                callback_result = self.callback(response)
        else:
            callback_result = None

        return callback_result, response

    async def _close_request_session(self):
        if self.close_request_session:
            await self.request_session.close()

    async def _make_request(self):
        self.logger.info(f"<{self.method}: {self.url}>")
        if self.method == 'GET':
            request_func = self.current_request_session.get(
                self.url, headers=self.headers, ssl=self.ssl, **self.kwargs)
        else:
            request_func = self.current_request_session.post(
                self.url, headers=self.headers, ssl=self.ssl, **self.kwargs)
        resp = await request_func
        return resp

    async def _retry(self, error_msg):
        if self.retry_times > 0:
            retry_times = self.request_config.get('RETRIES',
                                                  3) - self.retry_times + 1
            self.logger.error(
                f'<Retry url: {self.url}>, Retry times: {retry_times}, Retry message: {error_msg}>')
            self.retry_times -= 1
            retry_func = self.request_config.get('RETRY_FUNC')
            if retry_func and iscoroutinefunction(retry_func):
                request_ins = await retry_func(weakref.proxy(self))
                if isinstance(request_ins, Request):
                    return await request_ins.fetch()
            return await self.fetch()
        else:
            response = Response(
                url=self.url,
                method=self.method,
                metadata=self.metadata,
                cookies={},
                history=())

            return response

    def __repr__(self):
        return f"<{self.method} {self.url}>"
