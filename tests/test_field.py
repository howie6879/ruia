#!/usr/bin/env python

import os

import lxml

from ruia import AttrField, ElementField, TextField, HtmlField, RegexField
from ruia.field import NothingMatchedError

html_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "data", "for_field_testing.html"
)
with open(html_path, mode="r", encoding="utf-8") as file:
    HTML = file.read()

html_etree = lxml.etree.HTML(HTML)


def test_element_field():
    element_field = ElementField(css_select="div.brand a")
    value = element_field.extract(html_etree=html_etree)
    assert type(value) == lxml.etree._Element


def test_css_select():
    field = TextField(css_select="head title")
    value = field.extract(html_etree=html_etree)
    assert value == "ruia"


def test_xpath_select():
    field = TextField(xpath_select="/html/head/title")
    value = field.extract(html_etree=html_etree)
    assert value == "ruia"


def test_xpath_text_select():
    field = TextField(xpath_select="/html/head/title/text()")
    value = field.extract(html_etree=html_etree)
    assert value == "ruia"


def test_attr_field():
    attr_field = AttrField(css_select="div.brand a", attr="href")
    value = attr_field.extract(html_etree=html_etree)
    assert value == "https://github.com"


def test_text_field_many():
    field = TextField(css_select="a.test_link", many=True)
    values = field.extract(html_etree=html_etree)
    assert values[2] == "hello3 github."


def test_attr_field_many():
    field = AttrField(css_select="a.test_link", attr="href", many=True)
    values = field.extract(html_etree=html_etree)
    assert len(values) == 5
    assert values[3] == "https://github.com/howie6879/ruia"


def test_text_field_not_exist():
    field = TextField(css_select="nothing matched")
    try:
        field.extract(html_etree=html_etree)
    except Exception as e:
        assert isinstance(e, NothingMatchedError)


def test_attr_field_not_exist():
    field = TextField(css_select="nothing matched")
    try:
        field.extract(html_etree=html_etree)
    except Exception as e:
        assert isinstance(e, NothingMatchedError)


def test_text_field_many_even_there_is_only_one_in_html():
    field = TextField(css_select="div.brand a", many=True)
    value = field.extract(html_etree=html_etree)
    assert value[0] == "Github"


def test_attr_field_many_even_there_is_only_one_in_html():
    field = AttrField(css_select="div.brand a", attr="href", many=True)
    value = field.extract(html_etree=html_etree)
    assert value[0] == "https://github.com"
    assert len(value) == 1


def test_text_field_with_default():
    field = TextField(css_select="div.brand b", default="nothing")
    value = field.extract(html_etree=html_etree)
    assert value == "nothing"


def test_attr_field_with_default():
    field = AttrField(css_select="div.brand b", attr="href", default="nothing")
    value = field.extract(html_etree=html_etree)
    assert value == "nothing"


def test_text_field_with_default_and_many():
    field = TextField(css_select="div.brand b", default="nothing", many=True)
    values = field.extract(html_etree=html_etree)
    assert values == ["nothing"]


def test_attr_field_with_default_and_many():
    field = AttrField(
        css_select="div.brand b", attr="href", default="nothing", many=True
    )
    values = field.extract(html_etree=html_etree)
    assert values == ["nothing"]


def test_text_field_with_list_default_and_many():
    field = TextField(css_select="div.brand b", default=[], many=True)
    values = field.extract(html_etree=html_etree)
    assert values == []


def test_html_field():
    field_en = HtmlField(css_select="div.brand a")
    field_zh = HtmlField(css_select="div.brand p")
    assert (
        field_en.extract(html_etree=html_etree)
        == '<a href="https://github.com">Github</a>'
    )
    assert field_zh.extract(html_etree=html_etree) == "<p>你好</p>\n"


def test_html_field_with_many():
    field = HtmlField(css_select="a.test_link", many=True)
    values = field.extract(html_etree=html_etree)
    assert len(values) == 5
    assert (
        values[0]
        == '<a class="test_link" href="https://github.com/howie6879/">hello1 github.</a>\n'
    )
    assert (
        values[4]
        == '<a class="test_link" href="https://github.com/howie6879/">hello5 github.</a>\n'
        "    Some text outside.\n"
    )


def test_re_field_with_one_group():
    field = RegexField(re_select="<title>(.*?)</title>")
    href = field.extract(html=HTML)
    assert href == "ruia"


def test_re_field_with_no_group():
    field = RegexField(re_select="<title>.*?</title>")
    href = field.extract(html=HTML)
    assert href == "<title>ruia</title>"


def test_re_field_with_many_groups():
    field = RegexField(re_select='<h1><a href="(.*?)">(.*?)</a></h1>')
    href, text = field.extract(html=HTML)
    assert href == "https://github.com"
    assert text == "Github"


def test_re_field_with_named_groups():
    field = RegexField(re_select='<h1><a href="(?P<href>.*?)">(?P<text>.*?)</a></h1>')
    result = field.extract(html=HTML)
    assert result["href"] == "https://github.com"
    assert result["text"] == "Github"


def test_re_field_with_default():
    field = RegexField(re_select="nothing to match.", default="default value")
    result = field.extract(html=HTML)
    assert result == "default value"


def test_re_field_get_nothing_with_no_default():
    field = RegexField(re_select="nothing to match.")
    try:
        field.extract(html=HTML)
    except Exception as e:
        assert isinstance(e, NothingMatchedError)


def test_re_field_with_many():
    field = RegexField(
        re_select='<a class="test_link" href="(.*?)">(.*?)</a>', many=True
    )
    matches = field.extract(html=HTML)
    assert len(matches) == 5
    href0, text0 = matches[0]
    href4, text4 = matches[4]
    assert href0 == "https://github.com/howie6879/"
    assert text0 == "hello1 github."
    assert href4 == "https://github.com/howie6879/"
    assert text4 == "hello5 github."


def test_re_field_in_dict_format_with_many():
    field = RegexField(
        re_select='<a class="test_link" href="(?P<href>.*?)">(?P<text>.*?)</a>',
        many=True,
    )
    matches = field.extract(html=HTML)
    assert len(matches) == 5
    assert matches[0]["href"] == "https://github.com/howie6879/"
    assert matches[0]["text"] == "hello1 github."
    assert matches[4]["href"] == "https://github.com/howie6879/"
    assert matches[4]["text"] == "hello5 github."


def test_re_field_with_html_element():
    field = RegexField(re_select='<h1><a href="(?P<href>.*?)">(?P<text>.*?)</a></h1>')
    result = field.extract(html=html_etree)
    assert result["href"] == "https://github.com"
    assert result["text"] == "Github"
