#!/usr/bin/env python
from lxml import etree
from copy import deepcopy


class BaseField(object):
    """
    BaseField class
    """

    def __init__(self, css_select=None, xpath_select=None, default='', many=False):
        """
        Init BaseField class
        url: http://lxml.de/index.html
        :param css_select: css select http://lxml.de/cssselect.html
        :param xpath_select: http://www.w3school.com.cn/xpath/index.asp
        :param default: default value
        :param many: if there are many fields in one page
        """
        self.css_select = css_select
        self.xpath_select = xpath_select
        self.default = default
        self.many = many


class _LxmlElementField(BaseField):
    def _get_elements(self, html):
        if self.css_select:
            elements = html.cssselect(self.css_select)
        elif self.xpath_select:
            elements = html.xpath(self.xpath_select)
        else:
            raise ValueError('%s field: css_select or xpath_select is expected' % self.__class__.__name__)
        if not self.many:
            elements = elements[:1]
        return elements

    def _parse_element(self, element):
        raise NotImplementedError

    def extract_value(self, html, is_source=False):
        elements = self._get_elements(html)
        if is_source:
            return elements if self.many else elements[0]
        results = [self._parse_element(element) for element in elements]
        if self.many:
            return results
        else:
            return results[0] if results else ''


class TextField(_LxmlElementField):
    def _parse_element(self, element):
        strings = [node.strip() for node in element.itertext()]
        string = ''.join(strings)
        return string if string else self.default


class AttrField(_LxmlElementField):
    def __init__(self, attr, css_select=None, xpath_select=None, default='', many=False):
        super(AttrField, self).__init__(
            css_select=css_select, xpath_select=xpath_select, default=default, many=many)
        self.attr = attr

    def _parse_element(self, element):
        return element.get(self.attr, self.default)
