#!/usr/bin/env python
"""
 Created by howie.hu at 2018/7/13.
"""

from lxml import etree


class Response(object):
    """
    Return a friendly response
    """

    def __init__(self, url: str, extra_value: dict, status=200, headers=None, body=b'', content_type='text/plain',
                 charset='utf-8'):
        self._url = url
        self._extra_value = extra_value
        self._status = int(status)
        self._headers = headers
        self._body = body
        self._content_type = content_type
        self._charset = charset

    @property
    def e_html(self):
        e_html = None
        if self._body:
            e_html = etree.HTML(self._body)
        return e_html

    def __str__(self):
        return f'<Response url[{self._content_type}]: {self._url}, extra_value:{self._extra_value}>'
