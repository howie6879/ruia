#!/usr/bin/env python

from lxml import etree


class BaseField(object):
    """
    BaseField class
    """

    def __init__(self, css_select=None, xpath_select=None, default=None):
        """
        Init BaseField class
        url: http://lxml.de/index.html
        :param css_select: css select http://lxml.de/cssselect.html
        :param xpath_select: http://www.w3school.com.cn/xpath/index.asp
        :param default: default value
        """
        self.css_select = css_select
        self.xpath_select = xpath_select
        self.default = default


class TextField(BaseField):
    """
    TextField class for a field
    """

    def __init__(self, css_select=None, xpath_select=None, default=None):
        super(TextField, self).__init__(css_select, xpath_select, default)

    def extract_value(self, html, is_source=False):
        """
        Use css_select or re_select to extract a field value
        :return:
        """
        if self.css_select:
            value = html.cssselect(self.css_select)
        elif self.xpath_select:
            value = html.xpath(self.xpath_select)
        else:
            raise ValueError('%s field: css_select or xpath_select is expected' % self.__class__.__name__)
        if is_source:
            return value
        if isinstance(value, list) and len(value) == 1:
            text = ''
            if isinstance(value[0], etree._Element):
                for node in value[0].itertext():
                    text += node.strip()
            if isinstance(value[0], str) or isinstance(value[0], etree._ElementUnicodeResult):
                text = ''.join(value)
            value = text
        if self.default is not None:
            value = value if value else self.default
        return value


class AttrField(BaseField):
    """
    AttrField class for a field
    """

    def __init__(self, attr, css_select=None, xpath_select=None, default=None):
        super(AttrField, self).__init__(css_select, xpath_select, default)
        self.attr = attr

    def extract_value(self, html, is_source=False):
        """
        Use css_select or re_select to extract a field value
        :return:
        """
        if self.css_select:
            value = html.cssselect(self.css_select)
            value = value[0].get(self.attr, value) if len(value) == 1 else value
        elif self.xpath_select:
            value = html.xpath(self.xpath_select)
        else:
            raise ValueError('%s field: css_select or xpath_select is expected' % self.__class__.__name__)
        if is_source:
            return value
        if self.default is not None:
            value = value if value else self.default
        return value
