# An Overview of Ruia

Ruia is An asynchronous web scraping micro-framework,
powered by `asyncio` and `aiohttp`, 
aims at making crawling url as convenient as possible.

**Write less, run faster** is Ruia's philosophy.

Ruia spider consists only two **required** parts and three **optional** parts:

* Required:
    * [Fields](field.md), extract text or attribute from HTML;
    * [Items](item.md), a collection of fields;

* Optional:
    * [Spider](spider.md), a manager to make your spider stronger;
    * [Middleware](middleware.md), used for processing request and response;
    * [Plugin](plugins.md), used for enhancing ruia functions.

Ruia also provides friendly [Request](request.md) and [Response](response.md) objects.

Follow the links to learn each part of this tutorial.

For a simple spider, you may only need to learn [fields](field.md) and [Items](item.md),
and here is a concise example ([source][concise_hack_news_spider]):

```python
# Python 3.7 required
import asyncio
from ruia import Item, TextField, AttrField


class HackerNewsItem(Item):
    target_item = TextField(css_select='tr.athing')
    title = TextField(css_select='a.storylink')
    url = AttrField(css_select='a.storylink', attr='href')


async def parse_one_page(page):
    url = f'https://news.ycombinator.com/news?p={page}'
    return await HackerNewsItem.get_items(url=url)


async def main():
    coroutine_list = [parse_one_page(page) for page in range(1, 3)]
    result = await asyncio.gather(*coroutine_list)
    news_list = list()
    for one_page_list in result:
        news_list.extend(one_page_list)
    for news in news_list:
        print(news.title, news.url)


if __name__ == '__main__':
    asyncio.run(main())

```

[concise_hack_news_spider]: https://github.com/howie6879/ruia/blob/master/examples/concise_hacker_news_spider/main.py
