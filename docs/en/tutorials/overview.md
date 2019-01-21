# An Overview of Ruia

Ruia is An asynchronous web scraping micro-framework,
powered by `asyncio` and `aiohttp`, 
aims at making crawling url as convenient as possible.

**Write less, run faster** is Ruia's philosophy.

Ruia spider consists only two **required** parts and three **optional** parts:

* Required:
    * [Fields](field.md), extract text or attribute from HTML
    * [Items](item.md), a collection of fields

* Optional:
    * [Spider](spider.md), a manager to make your spider stronger
    * [Middleware](middleware.md), used for processing request and response
    * [Plugin](plugins.md), used for enhancing ruia functions

Ruia also provides friendly [Request](request.md) and [Response](response.md) objects, follow the links to learn each part of this tutorial.

For a simple spider, you may only need to learn [fields](field.md) and [Items](item.md),
and here is a concise example:

```python
#!/usr/bin/env python
"""
 Target: https://news.ycombinator.com/
"""
import asyncio

from ruia import AttrField, TextField, Item


class HackerNewsItem(Item):
    target_item = TextField(css_select='tr.athing')
    title = TextField(css_select='a.storylink')
    url = AttrField(css_select='a.storylink', attr='href')

    async def clean_title(self, value):
        return value


async def single_page_demo():
    items = await HackerNewsItem.get_items(url="https://news.ycombinator.com/")
    for item in items:
        print(item.title, item.url)
            
if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(single_page_demo())

```

More details: [hacker_news_item](https://github.com/howie6879/ruia/blob/master/examples/topics_examples/hacker_news_item.py)