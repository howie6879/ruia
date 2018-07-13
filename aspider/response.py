#!/usr/bin/env python
"""
 Created by howie.hu at 2018/7/13.
"""

from lxml import etree


class Response:
    """
    Return a friendly response
    """

    def __init__(self, html: str, url: str, extra_value: dict, res_type: str) -> None:
        self.html = html
        self.url = url
        self.extra_value = extra_value
        self.res_type = res_type

    @property
    def e_html(self):
        e_html = None
        if self.html:
            e_html = etree.HTML(self.html)
        return e_html

    def __str__(self):
        return f'<Response url[{self.res_type}]: {self.url}, extra_value:{self.extra_value}>'
