# Selector

`Selector` is implemented by `Field` class, and provides two ways for developers to extract data:
`CSS Selector` and `XPath Selector`.

In detail, they are implemented by the following three classes: 

- [AttrField(BaseField)][field.py]: extract property of HTML tag
- [TextField(BaseField)][field.py]: extract text data of HTML tag
- [HtmlField(BaseField)][field.py]: extract raw html code from HTML tag

## Core arguments

Arguments of all `Field` classes:
- default: str, default value, recommended, without which, will raise an Error when trying to get a non exist value.
- many: bool, the return value will be a list.


Arguments shard by `TextField`, `AttrField` and `HtmlField`:
- css_select: locate the HTML tag by css selector.
- xpath_select: locate the HTML tag by xpath selector.

`AttrField` requires an extra field:
- attr: the target attribute name of HTML tag.

`RegexField` requires an extra field:
- re_select: an regular expression, should be a str object.

## Usage

```python
from lxml import etree
from ruia import AttrField, TextField, HtmlField, RegexField

HTML = """
<html>
    <head>
        <title>ruia</title>
    </head>
    <body>¬
        <p>
            <a class="test_link" href="https://github.com/howie6879/ruia">hello github.</a>
        </p>
    </body>
</html>
"""

html = etree.HTML(HTML)


def test_css_select():
    field = TextField(css_select="head title")
    value = field.extract(html_etree=html)
    assert value == "ruia"


def test_xpath_select():
    field = TextField(xpath_select='/html/head/title')
    value = field.extract(html_etree=html)
    assert value == "ruia"


def test_attr_field():
    attr_field = AttrField(css_select="p a.test_link", attr='href')
    value = attr_field.extract(html_etree=html)
    assert value == "https://github.com/howie6879/ruia"

def test_html_field():
    field = HtmlField(css_select="a.test_link")
    assert field.extract(html_etree=html) == '<a class="test_link" href="https://github.com/howie6879/ruia">hello github.</a>'

def test_re_field():
    field = RegexField(re_select='<title>(.*?)</title>')
    href = field.extract(html=HTML)
    assert href == 'ruia'

```

## How It Works?

Use `lxml` to extract data from HTML source code, in terms of `CSS Selector` or `XPath Selector`.

### About RegexField

`RegexField` is only used for better performance.
It directly use python standard library `re`,
so it's significantly faster than other fields implemented on lxml.
If you only want to use regular expression to clean your crawled string,
please use `clean_` methods of Item, and here is an example:

```python
import re
import ruia

class MyItem(ruia.Item):
    title = ruia.TextField(css_select='title')
    
    def clean_title(self, value):
        return re.match('Blog: (.*?)', value).group(0)

```

`RegexField` do not use lxml to parse source code,
so there's no `css_select` and `xpath_select` for `RegexField`.

`RegexField` has a complex behaviour:

- if you set many=`False`:
    - if you use **named group** in your regular expression, return a dictionary;
    - else if you use **group** in your regular expression
        - if there's only **one group**, return the group value as a string;
        - if there are **many groups**, return a tuple of the values;
    - else, return the whole match string.
    
- if you set many=`True`:
    - return a list of the return values above.

!!! Note
    if you use named group, those groups without names will be lost.


[field.py]: https://github.com/howie6879/ruia/blob/master/ruia/field.py
