#!/usr/bin/env python

import pytest

from lxml import etree

from ruia import AttrField, TextField
from ruia.field import NothingMatchedError

HTML = """
<html>
    <head>
        <title>ruia</title>
    </head>
    <body>¬
    <div class="brand">
        <h1><a href="https://github.com">Github</a></h1>
    </div>
        <p>
            <a class="test_link" href="https://github.com/howie6879/">hello1 github.</a>
        </p>        
        <p>
            <a class="test_link" href="https://github.com/howie6879/">hello2 github.</a>
        </p>        
        <p>
            <a class="test_link" href="https://github.com/howie6879/">hello3 github.</a>
        </p>        
        <p>
            <a class="test_link" href="https://github.com/howie6879/ruia">hello4 github.</a>
        </p>        
        <p>
            <a class="test_link" href="https://github.com/howie6879/">hello5 github.</a>
        </p>
    </body>
</html>
"""

html_etree = etree.HTML(HTML)


def test_css_select():
    field = TextField(css_select="head title")
    value = field.extract_value(html_etree=html_etree)
    assert value == "ruia"


def test_xpath_select():
    field = TextField(xpath_select='/html/head/title')
    value = field.extract_value(html_etree=html_etree)
    assert value == "ruia"


def test_attr_field():
    attr_field = AttrField(css_select="div.brand a", attr='href')
    value = attr_field.extract_value(html_etree=html_etree)
    assert value == "https://github.com"


def test_text_field_many():
    field = TextField(css_select="a.test_link", many=True)
    values = field.extract_value(html_etree=html_etree)
    assert values[2] == 'hello3 github.'


def test_attr_field_many():
    field = AttrField(css_select="a.test_link", attr="href", many=True)
    values = field.extract_value(html_etree=html_etree)
    assert values[3] == "https://github.com/howie6879/ruia"


def test_text_field_not_exist():
    field = TextField(css_select="nothing matched")
    value = field.extract_value(html_etree=html_etree)
    assert value==''


def test_attr_field_not_exist():
    field = TextField(css_select="nothing matched")
    value = field.extract_value(html_etree=html_etree)
    assert value == ''


def test_text_field_many_even_there_is_only_one_in_html():
    field = TextField(css_select="div.brand a", many=True)
    value = field.extract_value(html_etree=html_etree)
    assert value[0] == 'Github'


def test_attr_field_many_even_there_is_only_one_in_html():
    field = AttrField(css_select="div.brand a", attr="href", many=True)
    value = field.extract_value(html_etree=html_etree)
    assert value[0] == 'https://github.com'


def test_text_field_with_default():
    field = TextField(css_select="div.brand b", default='nothing')
    value = field.extract_value(html_etree=html_etree)
    assert value == 'nothing'


def test_attr_field_with_default():
    field = AttrField(css_select="div.brand b", attr='href', default='nothing')
    value = field.extract_value(html_etree=html_etree)
    assert value == 'nothing'


def test_text_field_with_default_and_many():
    field = TextField(css_select="div.brand b", default="nothing", many=True)
    values = field.extract_value(html_etree=html_etree)
    assert values == ['nothing']


def test_attr_field_with_default_and_many():
    field = AttrField(css_select="div.brand b", attr="href", default="nothing", many=True)
    values = field.extract_value(html_etree=html_etree)
    assert values == ['nothing']

if __name__ == '__main__':
    test_attr_field_with_default_and_many()