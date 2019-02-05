# Selector

`Selector`通过`Field`类实现，为开发者提供了`CSS Selector`和`XPath`两种方式提取目标数据，具体由下面两个类实现：
- [AttrField(BaseField)](https://github.com/howie6879/ruia/blob/master/ruia/field.py)：提取网页标签的属性数据
- [TextField(BaseField)](https://github.com/howie6879/ruia/blob/master/ruia/field.py)：提取网页标签的text数据

## Core arguments

所有的`Field`共有的参数：
- default: str, 设置默认值，建议定义，否则找不到字段时会报错
- many: bool, 返回值将是一个列表

`AttrField`、`TextField`、`HtmlField`共用参数：
- css_select：str, 利用`CSS Selector`提取目标数据
- xpath_select：str, 利用`XPath`提取目标数据

`AttrField`需要一个额外的参数：
- attr：目标标签属性

`RegexField`需要一个额外的参数：
- re_select: str, 正则表达式字符串

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

定好`CSS Selector`或`XPath`规则，然后利用`lxml`实现对目标`html`进行目标数据的提取

### 关于`RegexField`

详细信息请参阅[英文文档][fields_doc_en]。
 
[fields_doc_en]: https://github.com/howie6879/ruia/blob/master/docs/en/topics/selector.md