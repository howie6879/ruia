# Spider Control

`ruia.Spider` is used to control the whole spider,
it provides the following functions:

* Normalize your code;
* Maintain a event loop;
* Manage requests and responses;
* Concurrency control;
* Manage middlewares and plugins.

Although it works well,
to use only `ruia.Item` to create a spider,
`ruia` recommend to use `ruia.Spider` to implement a stronger spider.

## Normalize your code

`ruia.Spider` requires a class property `start_urls` as the entry point of a spider.
Inner, `ruia` will iterate `start_urls`,
and send a request to server for each request.
After receiving server response,
`ruia` will call `spider.parse(response)`,
and this is the main part of your spider.

Here's a simple parse example, to simply save response fields to a text file.
We only have to define `start_urls`,
and implement a `parst` method.

```python
import aiofiles

from ruia import Spider, Item, TextField, AttrField


class HackerNewsItem(Item):
    target_item = TextField(css_select='tr.athing')
    title = TextField(css_select='a.storylink')
    url = AttrField(css_select='a.storylink', attr='href')

class HackerNewsSpider(Spider):
    start_urls = [f'https://news.ycombinator.com/news?p={index}' for index in range(3)]

    async def parse(self, res):
        items = await HackerNewsItem.get_items(html=res.html)
        for item in items:
            async with aiofiles.open('./hacker_news.txt', mode='a', encoding='utf-8') as f:
                await f.write(item.title + '\n')

```

`aiofiles` is a third-party library to operate files in asynchronous way.
It provides APIs the same as python standard `open` function.

Now, we have written a spider,
and time to start crawling.

```python
import aiofiles

from ruia import Spider, Item, TextField, AttrField


class HackerNewsItem(Item):
    target_item = TextField(css_select='tr.athing')
    title = TextField(css_select='a.storylink')
    url = AttrField(css_select='a.storylink', attr='href')

class HackerNewsSpider(Spider):
    start_urls = [f'https://news.ycombinator.com/news?p={index}' for index in range(3)]

    async def parse(self, res):
        items = await HackerNewsItem.get_items(html=res.html)
        for item in items:
            async with aiofiles.open('./hacker_news.txt', mode='a', encoding='utf-8') as f:
                await f.write(item.title + '\n')

if __name__ == '__main__':
    HackerNewsSpider.start()

``` 

Done.

## Send Further Requests

## Concurrency Control

## Use Middleware and Plugin
