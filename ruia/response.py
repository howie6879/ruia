"""
    Created by howie.hu at 2022-08-21.
    Description: Return a friendly response
    Changelog: all notable changes to this file will be documented
"""

import asyncio
import json

from http.cookies import SimpleCookie
from typing import Any, Callable, Optional

from lxml import etree

try:
    import uvloop

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass

DEFAULT_JSON_DECODER = json.loads
JSONDecoder = Callable[[str], Any]


class Response(object):
    """
    Return a friendly response
    """

    def __init__(
        self,
        url: str,
        method: str,
        *,
        encoding: str = "",
        metadata: dict,
        cookies,
        history,
        headers,
        status: int = -1,
        aws_json: Callable = None,
        aws_read: Callable = None,
        aws_text: Callable = None,
    ):
        self._callback_result = None
        self._encoding = encoding
        self._url = url
        self._method = method
        self._metadata = metadata
        self._index = None
        self._html = ""
        self._cookies = cookies
        self._history = history
        self._headers = headers
        self._status = status
        self._ok = self._status == 0 or 200 <= self._status <= 299

        self._aws_json = aws_json
        self._aws_read = aws_read
        self._aws_text = aws_text

    @property
    def callback_result(self):
        """Return callback_result"""
        return self._callback_result

    @callback_result.setter
    def callback_result(self, value):
        self._callback_result = value

    @property
    def index(self):
        """Return index"""
        return self._index

    @index.setter
    def index(self, value):
        self._index = value

    @property
    def ok(self) -> bool:
        """Return ok status"""
        return self._ok

    @ok.setter
    def ok(self, value: bool):
        self._ok = value

    @property
    def encoding(self):
        """Return encoding"""
        return self._encoding

    @property
    def url(self):
        """Return url"""
        return self._url

    @property
    def method(self):
        """Return method"""
        return self._method

    @property
    def metadata(self):
        """Return metadata"""
        return self._metadata

    @property
    def cookies(self) -> dict:
        """Return cookies"""
        if isinstance(self._cookies, SimpleCookie):
            cur_cookies = {}
            for key, value in self._cookies.items():
                cur_cookies[key] = value.value
            return cur_cookies
        else:
            return self._cookies

    @property
    def history(self):
        """Return history"""
        return self._history

    @property
    def headers(self):
        """Return headers"""
        return self._headers

    @property
    def status(self):
        """Return status"""
        return self._status

    def html_etree(self, html: str, **kwargs):
        """
        Return etree HTML
        """
        html = html or self._html
        html_etree = etree.HTML(text=html, **kwargs)
        return html_etree

    async def json(
        self,
        *,
        encoding: str = None,
        loads: JSONDecoder = DEFAULT_JSON_DECODER,
        content_type: Optional[str] = "application/json",
    ) -> Any:
        """Read and decodes JSON response."""
        encoding = encoding or self._encoding
        return await self._aws_json(
            encoding=encoding, loads=loads, content_type=content_type
        )

    async def read(self) -> bytes:
        """Read response payload."""
        return await self._aws_read()

    async def text(
        self, *, encoding: Optional[str] = None, errors: str = "strict"
    ) -> str:
        """Read response payload and decode."""
        encoding = encoding or self._encoding
        self._html = await self._aws_text(encoding=encoding, errors=errors)
        return self._html

    def __repr__(self):
        return f"<Response url[{self._method}]: {self._url} status:{self._status}>"
