#!/usr/bin/env python

from lxml import etree


class Response(object):
    """
    Return a friendly response
    """

    def __init__(self, url: str, *,
                 metadata: dict,
                 res_type: str,
                 html: str = '',
                 cookies,
                 history,
                 headers: dict = None,
                 status: int):
        self._url = url
        self._metadata = metadata
        self._res_type = res_type
        self._html = html
        self._cookies = cookies
        self._history = history
        self._headers = headers
        self._status = status

    @property
    def url(self):
        return self._url

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
    def e_html(self):
        e_html = None
        if self.html:
            e_html = etree.HTML(self.html)
        return e_html

    def __str__(self):
        return f'<Response url[{self._res_type}]: {self._url} status:{self._status} metadata:{self._metadata}>'
