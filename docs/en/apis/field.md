# Define Data with Fields

## Overview

Fields are used to extract value from HTML code.

Ruia supports the following fields:

* `TextField`: extract text string of the selected HTML element
* `AttrField`: extract an attribute of the selected HTML element
* `HtmlField`: extract raw HTML code of the selected HTML element
* `RegexField`: use standard library `re` for better performance

!!! Note
    All the parameters of fields are **keyword arguments**.

## TextField

`TextField` first select an HTML element by CSS Selector or XPath Selector,
then get the text value of the selected element.

### Parameters

* `css_select`: `str`, alternative, match HTML element(s) with CSS Selector
* `xpath_select`: `str`, alternative, match HTML element(s) with XPath Selector
* `default`: `str`, recommended, the default value if nothing matched in HTML element
* `many`: `bool`, optional, extract a list if True

### Example

```python
import ruia

from lxml import etree

HTML = '''
<body>
<div class="title">Ruia Documentation</div>
<ul>
    <li class="tag" href="./easy.html">easy</li>
    <li class="tag" href="./fast.html">fast</li>
    <li class="tag" href="./powerful.html">powerful</li>
</ul>
</body>
'''


html = etree.HTML(HTML)

def test_text_field():
    title_field = ruia.TextField(css_select='.title', default='Untitled')
    assert title_field.extract(html_etree=html) == 'Ruia Documentation'
    tag_field = ruia.TextField(css_select='.tag', default='No tag', many=True)
    assert tag_field.extract(html_etree=html) == ['easy', 'fast', 'powerful']

```


## AttrField

`TextField` first select an HTML element by CSS Selector or XPath Selector,
then get the attribute value of the selected element.

### Parameters

* `attr`: `str`, required, the name of the attribute you want to extract
* `css_select`: `str`, alternative, match HTML element(s) with CSS Selector
* `xpath_select`: `str`, alternative, match HTML element(s) with XPath Selector
* `default`: `str`, recommended, the default value if nothing matched in HTML element
* `many`: `bool`, optional, extract a list if True

### Example

```python
import ruia

from lxml import etree

HTML = '''
<body>
<div class="title" href="/">Ruia Documentation</div>
<ul>
    <li class="tag" href="./easy.html">easy</li>
    <li class="tag" href="./fast.html">fast</li>
    <li class="tag" href="./powerful.html">powerful</li>
</ul>
</body>
'''

html = etree.HTML(HTML)

def test_attr_field():
    title = ruia.AttrField(css_select='.title', attr='href', default='Untitled')
    assert title.extract(html_etree=html) == '/'
    tags = ruia.AttrField(css_select='.tag', attr='href', default='No tag', many=True)
    assert tags.extract(html_etree=html)[0] == './easy.html'

```

## HtmlField

`TextField` first select an HTML element by CSS Selector or XPath Selector,
then get the raw HTML code of the selected element.

If there's some spaces or some text outside any HTML elements between this element and next element,
then this part of text will also inside the return value.
It's an unstable feature, perhaps in later versions the outside text will be remove by default.

### Parameters

* `css_select`: `str`, alternative, match HTML element(s) with CSS Selector
* `xpath_select`: `str`, alternative, match HTML element(s) with XPath Selector
* `default`: `str`, recommended, the default value if nothing matched in HTML element
* `many`: `bool`, optional, extract a list if True

### Example

```python
import ruia

from lxml import etree

HTML = '''
<body>
<div class="title">Ruia Documentation</div>
<ul>
    <li class="tag" href="./easy.html">easy</li>
    <li class="tag" href="./fast.html">fast</li>
    <li class="tag" href="./powerful.html">powerful</li>
</ul>
</body>
'''

html = etree.HTML(HTML)

def test_html_field():
    title = ruia.HtmlField(css_select='.title', default='Untitled')
    assert title.extract(html_etree=html) == '<div class="title" href="/">Ruia Documentation</div>\n'
    tags = ruia.HtmlField(css_select='.tag', default='No tag', many=True)
    assert tags.extract(html_etree=html)[1] == '<li class="tag" href="./fast.html">fast</li>\n    '

```

## RegexField

`TextField` do not parse html structure,
it directly use python standard library `re`.
If your spider meets performance limitation, try `RegexField`.
However, `ruia` is based on `asyncio`,
you will seldom meet performance limitation!

`RegexField` has a complex behaviour:

* if no group: return the whole matched string
* if regex has a group: return the group value
* if regex has multiple groups: return a list a string
* if regex has named groups, no matter one or more: return a dict, whose key and value are both string
* if `many=True`, return a list of above values

### Parameters

* `re_select`: `str`, required, match HTML element(s) with regular expression
* `default`: `str`, recommended, the default value if nothing matched in HTML element
* `many`: `bool`, optional, extract a list if True

### Example

```python
import ruia

from lxml import etree

HTML = '''
<body>
<div class="title" href="/">Ruia Documentation</div>
<ul>
    <li class="tag" href="./easy.html">easy</li>
    <li class="tag" href="./fast.html">fast</li>
    <li class="tag" href="./powerful.html">powerful</li>
</ul>
</body>
'''

html = etree.HTML(HTML)

def test_regex_field():
    title = ruia.RegexField(re_select='<div class="title" href="(.*?)">(.*?)</div>')
    assert title.extract(html=HTML)[0] == '/'
    assert title.extract(html=HTML)[1] == 'Ruia Documentation'
    tags = ruia.RegexField(re_select='<li class="tag" href="(?P<href>.*?)">(?P<text>.*?)</li>', many=True)
    result = tags.extract(html=HTML)
    assert isinstance(result, list)
    assert len(result) == 3
    assert isinstance(result[0], dict)
    assert result[0]['href'] == './easy.html'

```

### About Parameter many
 
 Parameter `many=False` indicates if the field will extract one value or multiple values from HTML source code.
 
 For example, one Github Issue has many tags,
 We can use `Item.get_items` to get multiple values of tags,
 but that means an extra class definition.
 Parameter `many` aims to solve this problem.
 
A field is default by `many=False`,
that means, for `TextField`, `AttrField` and `HtmlField`,
`Field.extract(*, **)` will always return a string,
and `RegexField` will return a string or a list or dict,
depending on whether there are groups in the regular expression.
We can consider it with a 'singular number'.

With `many=True`, each field will return a 'plural',
that is, return a list.