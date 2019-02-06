#!/usr/bin/env python

from lxml import etree
import json


class Response(object):
    """
    Return a friendly response
    """

    def __init__(self, url: str, method: str, *,
                 metadata: dict,
                 res_type: str,
                 html: str = '',
                 cookies,
                 history,
                 headers: dict = None,
                 status: int):
        self._callback_result = None
        self._url = url
        self._method = method
        self._metadata = metadata
        self._res_type = res_type
        self._html = html
        self._index = None
        self._cookies = cookies
        self._history = history
        self._headers = headers
        self._status = status

    @property
    def callback_result(self):
        return self._callback_result

    @callback_result.setter
    def callback_result(self, value):
        self._callback_result = value

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, value):
        self._index = value

    @property
    def url(self):
        return self._url

    @property
    def method(self):
        return self._method

    @property
    def metadata(self):
        return self._metadata

    @property
    def res_type(self):
        return self._res_type

    @property
    def html(self):
        return self._html

    @property
    def cookies(self):
        return self._cookies

    @property
    def history(self):
        return self._history

    @property
    def headers(self):
        return self._headers

    @property
    def status(self):
        return self._status

    @property
    def html_etree(self):
        html_etree = None
        if self.html:
            html_etree = etree.HTML(self.html)
        return html_etree

    @property
    def json(self):
        return json.loads(self.html)

    def __str__(self):
        return f'<Response url[{self._method}]: {self._url} status:{self._status} html_type:{self._res_type}>'
