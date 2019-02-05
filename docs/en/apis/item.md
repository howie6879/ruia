# Item

`item` is mainly used to define data model and extract data from HTML source code.
It has the following two methods:

- [get_item][get_item]: extract one data from HTML source code
- [get_items][get_items]: extract many data from HTML source code

## Core arguments

`get_item` and `get_items` receives same arguments:
- html: optional, HTML source code
- url: optional, HTML href link
- html_etree: optional, etree._Element object

## Usage

From the arguments above, we can see that,
there are three ways to feed `Item` object: from a web link, from HTML source code, or even from `etree._Element` object.

```python
import asyncio

from ruia import AttrField, TextField, Item

class HackerNewsItem(Item):
    target_item = TextField(css_select='tr.athing')
    title = TextField(css_select='a.storylink')
    url = AttrField(css_select='a.storylink', attr='href')

    async def clean_title(self, value):
        return value

async def main():
    async for item in HackerNewsItem.get_items(url="https://news.ycombinator.com/"):
        print(item.title, item.url)

if __name__ == '__main__':
     items = asyncio.run(main())

```

Sometimes we may come across such a condition.
When crawling github issues, we will find that there are several tags to a issue.
Define `TagItem` as a standalone item is not that beautiful.
It's time to focus on the `many=True` argument.
Fields with `many=True` will return a list.

```python
from ruia import Item, TextField

class GithiubIssueItem(Item):
    issue_id = TextField(css_select='issue_id_class')
    title = TextField(css_select='issue_title_class')
    tags = TextField(css_select='tag_class',many=True)
    
    
item = GithiubIssueItem.get_item(html)
assert isinstance(item.tags, list)
```

`AttrField` also has the argument `many`.

### How It Works?

Inner, `item` class will change different kinds of inputs into `etree._Element` obejct, and then extract data.
`Meta class` will help to get every property defined by `Filed`.

[get_item]: https://github.com/howie6879/ruia/blob/master/ruia/item.py
[get_items]: https://github.com/howie6879/ruia/blob/master/ruia/item.py
