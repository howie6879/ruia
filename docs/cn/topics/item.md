# Item

`Item`的主要作用是定义以及通过一定的规则提取源网页中的目标数据，它主要提供一下两个方法：
- [get_item](https://github.com/howie6879/ruia/blob/master/ruia/item.py)：针对页面单目标数据进行提取
- [get_items](https://github.com/howie6879/ruia/blob/master/ruia/item.py)：针对页面多目标数据进行提取

## Core arguments

`get_item`和`get_items`方法接收的参数是一致的：
- html：网页源码
- url：网页链接
- html_etree：etree._Element对象

## Usage

通过上面的参数介绍可以知道，不论是源网站链接或者网站`HTML`源码，甚至是经过`lxml`处理过的`etree._Element`对象，`Item`能接收这三种类型的输入并进行处理

```python
import asyncio

from ruia import AttrField, TextField, Item

class HackerNewsItem(Item):
    target_item = TextField(css_select='tr.athing')
    title = TextField(css_select='a.storylink')
    url = AttrField(css_select='a.storylink', attr='href')

    async def clean_title(self, value):
        return value

async_func = HackerNewsItem.get_items(url="https://news.ycombinator.com/")
items = asyncio.get_event_loop().run_until_complete(async_func)
for item in items:
    print(item.title, item.url)

```

有时你会遇见这样一种情况，例如爬取Github的Issue时，你会发现一个Issue可能对应多个Tag。
这时，将Tag作为一个独立的`Item`来提取是不划算的，
我们可以使用`Field`字段的`many=True`参数，使这个字段返回一个列表。

```python
import asyncio
from ruia import Item, TextField, AttrField


class GithiubIssueItem(Item):
    title = TextField(css_select='title')
    tags = AttrField(css_select='a.IssueLabel', attr='data-name', many=True)


item = asyncio.run(GithiubIssueItem.get_item(url='https://github.com/pypa/pip/issues/72'))
assert isinstance(item.tags, list)
```

同样，`TextField`也支持`many`参数。

### How It Works?
最终`Item`类会将输入最终转化为`etree._Element`对象进行处理，然后利用元类的思想将每一个`Field`构造的属性计算为源网页上对应的真实数据
