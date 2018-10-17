#!/usr/bin/env python

import asyncio

import aiohttp
import async_timeout
import cchardet
import pyppeteer

from inspect import iscoroutinefunction
from types import AsyncGeneratorType
from typing import Tuple

try:
    import uvloop

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass

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
        'RETRY_FUNC': None
    }

    METHOD = ['GET', 'POST']

    def __init__(self, url: str, method: str = 'GET', *,
                 callback=None,
                 headers: dict = {},
                 load_js: bool = False,
                 metadata: dict = {},
                 request_config: dict = {},
                 request_session=None,
                 res_type: str = 'text',
                 **kwargs):
        # TODO: cookie
        """
        Initialization parameters
        """
        self.url = url
        self.method = method.upper()
        if self.method not in self.METHOD:
            raise ValueError('%s method is not supported' % self.method)

        self.callback = callback
        self.headers = headers
        self.load_js = load_js
        self.metadata = metadata if metadata is not None else {}
        self.request_session = request_session
        if request_config is None:
            self.request_config = self.REQUEST_CONFIG
        else:
            self.request_config = request_config
        self.res_type = res_type
        self.kwargs = kwargs

        self.close_request_session = False
        self.logger = get_logger(name=self.name)
        self.retry_times = self.request_config.get('RETRIES', 3)
        # self.setting = SettingsWrapper()

    @property
    def current_request_func(self):
        self.logger.info(f"<{self.method}: {self.url}>")
        if self.method == 'GET':
            request_func = self.current_request_session.get(
                self.url,
                headers=self.headers,
                verify_ssl=False,
                **self.kwargs
            )
        else:
            request_func = self.current_request_session.post(
                self.url,
                headers=self.headers,
                verify_ssl=False,
                **self.kwargs
            )
        return request_func

    @property
    def current_request_session(self):
        if self.request_session is None:
            self.request_session = aiohttp.ClientSession()
            self.close_request_session = True
        return self.request_session

    async def close(self):
        if hasattr(self, "browser"):
            await self.browser.close()
        if self.close_request_session:
            await self.request_session.close()
            self.request_session = None

    async def fetch(self) -> Response:
        if self.request_config.get('DELAY', 0) > 0:
            await asyncio.sleep(self.request_config['DELAY'])
        try:
            timeout = self.request_config.get('TIMEOUT', 10)

            if self.load_js:
                if not hasattr(self, "browser"):
                    self.browser = await pyppeteer.launch(headless=True, args=['--no-sandbox'])
                page = await  self.browser.newPage()
                res = await page.goto(self.url, options={'timeout': int(timeout * 1000)})
                data = await page.content()
                res_cookies = await page.cookies()
                res_headers = res.headers
                res_history = None
                res_status = res.status
            else:
                async with async_timeout.timeout(timeout):
                    async with self.current_request_func as resp:
                        res_status = resp.status
                        assert res_status in [200, 201]
                        if self.res_type == 'bytes':
                            data = await resp.read()
                        elif self.res_type == 'json':
                            data = await resp.json()
                        else:
                            content = await resp.read()
                            charset = cchardet.detect(content)
                            data = content.decode(charset['encoding'])
                        res_cookies, res_headers, res_history = resp.cookies, resp.headers, resp.history
        except Exception as e:
            res_headers = {}
            res_history = ()
            res_status = 0
            data, res_cookies = None, None
            self.logger.error(f"<Error: {self.url} {res_status} {str(e)}>")

        if self.retry_times > 0 and data is None:
            retry_times = self.request_config.get('RETRIES', 3) - self.retry_times + 1
            self.logger.info(f'<Retry url: {self.url}>, Retry times: {retry_times}')
            self.retry_times -= 1
            retry_func = self.request_config.get('RETRY_FUNC')
            if retry_func and iscoroutinefunction(retry_func):
                request_ins = await retry_func(self)
                if isinstance(request_ins, Request):
                    return await request_ins.fetch()
            return await self.fetch()

        await self.close()

        response = Response(url=self.url,
                            html=data,
                            metadata=self.metadata,
                            res_type=self.res_type,
                            cookies=res_cookies,
                            headers=res_headers,
                            history=res_history,
                            status=res_status)
        return response

    async def fetch_callback(self, sem) -> Tuple[AsyncGeneratorType, Response]:
        async with sem:
            res = await self.fetch()
        if self.callback is not None:
            try:
                if iscoroutinefunction(self.callback):
                    callback_res = await self.callback(res)
                    res.callback_result = callback_res
                else:
                    callback_res = self.callback(res)
            except Exception as e:
                self.logger.error(e)
                callback_res = None
        else:
            callback_res = None
        return callback_res, res

    def __str__(self):
        return "<%s %s>" % (self.method, self.url)
