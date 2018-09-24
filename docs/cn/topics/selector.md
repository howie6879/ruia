## Selector

`Selector`通过`Field`类实现，为开发者提供了`CSS Selector`和`XPath`两种方式提取目标数据，具体由下面两个类实现：
- [AttrField(BaseField)](https://github.com/howie6879/aspider/blob/master/aspider/field.py)：提取网页标签的属性数据
- [TextField(BaseField)](https://github.com/howie6879/aspider/blob/master/aspider/field.py)：提取网页标签的text数据

### Core arguments

对于`AttrField`，主要参数说明如下：
- css_select：利用`CSS Selector`提取目标数据
- xpath_select：利用`XPath`提取目标数据
- default：设置默认值

对于`TextField`，主要参数说明如下：
- attr：目标标签属性
- css_select：利用`CSS Selector`提取目标数据
- xpath_select：利用`XPath`提取目标数据
- default：设置默认值

### Usage

```python
from lxml import etree

from aspider import AttrField, TextField

HTML = """
<html>
    <head>
        <title>aspider</title>
    </head>
    <body>¬
        <p>
            <a class="test_link" href="https://github.com/howie6879/aspider">hello github.</a>
        </p>
    </body>
</html>
"""

html = etree.HTML(HTML)


def test_css_select():
    field = TextField(css_select="head title")
    value = field.extract_value(html)
    assert value == "aspider"


def test_xpath_select():
    field = TextField(xpath_select='/html/head/title')
    value = field.extract_value(html)
    assert value == "aspider"


def test_attr_field():
    attr_field = AttrField(css_select="p a.test_link", attr='href')
    value = attr_field.extract_value(html)
    assert value == "https://github.com/howie6879/aspider"
```

### How It Works?
定好`CSS Selector`或`XPath`规则，然后利用`lxml`实现对目标`html`进行目标数据的提取