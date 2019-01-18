## Selector

`Selector` is implemented by `Field` class, and provides two ways for developers to extract data:
`CSS Selector` and `XPath Selector`.

In detail, they are implemented by the following three classes: 

- [AttrField(BaseField)][field.py]: extract property of HTML tag
- [TextField(BaseField)][field.py]: extract text data of HTML tag
- [HtmlField(BaseField)][field.py]: extract raw html code from HTML tag

### Core arguments

Arguments of all `Field` classes:
- default: default value if no HTML tag founded.
- many: bool, the return value will be a list.


Arguments shard by `TextField`, `AttrField` and `HtmlField`:
- css_select: locate the HTML tag by css selector.
- xpath_select: locate the HTML tag by xpath selector.

`AttrField` requires an extra field:
- attr: the target attribute name of HTML tag.

### Usage

```python
from lxml import etree
from ruia import AttrField, TextField, HtmlField

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
    value = field.extract_value(html)
    assert value == "ruia"


def test_xpath_select():
    field = TextField(xpath_select='/html/head/title')
    value = field.extract_value(html)
    assert value == "ruia"


def test_attr_field():
    attr_field = AttrField(css_select="p a.test_link", attr='href')
    value = attr_field.extract_value(html)
    assert value == "https://github.com/howie6879/ruia"

def test_html_field():
    field = HtmlField(css_select="a.test_link")
    assert field.extract_value(html_etree=html) == '<a class="test_link" href="https://github.com/howie6879/ruia">hello github.</a>'

```

### How It Works?

Use `lxml` to extract data from HTML source code, in terms of `CSS Selector` or `XPath Selector`.

[field.py]: https://github.com/howie6879/ruia/blob/master/ruia/field.py
