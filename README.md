## Ruia

[![travis](https://travis-ci.org/howie6879/ruia.svg?branch=master)](https://travis-ci.org/howie6879/ruia) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ruia.svg)](https://pypi.org/project/ruia/) [![PyPI](https://img.shields.io/pypi/v/ruia.svg)](https://pypi.org/project/ruia/) [![license](https://img.shields.io/github/license/howie6879/ruia.svg)](https://github.com/howie6879/ruia)

### Overview

An async web scraping micro-framework, written with `asyncio` and `aiohttp`, aims to make crawling url as convenient as possible.

Write less, run faster:

- Documentation: [中文文档](https://github.com/howie6879/ruia/blob/master/docs/cn/README.md) |[documentation](https://github.com/howie6879/ruia/blob/master/docs/en/README.md)
- Plugins: [https://github.com/ruia-plugins](https://github.com/ruia-plugins)


### Installation

``` shell
# For Linux & Mac
pip install -U ruia[uvloop]

# For Windows
pip install -U ruia

# New features
pip install git+https://github.com/howie6879/ruia
```

### Usage

#### Request & Response

We provide an easy way to `request` a url and return a friendly `response`:

``` python
import asyncio

from ruia import Request

request = Request("https://news.ycombinator.com/")
response = asyncio.get_event_loop().run_until_complete(request.fetch())

# Output
# [2018-07-25 11:23:42,620]-Request-INFO  <GET: https://news.ycombinator.com/>
# <Response url[text]: https://news.ycombinator.com/ status:200 metadata:{}>
```

**JavaScript Support**:

``` python
request = Request("https://www.jianshu.com/", load_js=True)
response = asyncio.get_event_loop().run_until_complete(request.fetch())
print(response.body)
```

You need to pay attention when you use `load_js`, it will download a recent version of Chromium (~100MB). This only happens once.

#### Item

Let's take a look at a quick example of using `Item` to extract target data. Start off by adding the following to your demo.py:

``` python
import asyncio

from ruia import AttrField, TextField, Item


class HackerNewsItem(Item):
    target_item = TextField(css_select='tr.athing')
    title = TextField(css_select='a.storylink')
    url = AttrField(css_select='a.storylink', attr='href')

    async def clean_title(self, value):
        return value


items = asyncio.get_event_loop().run_until_complete(HackerNewsItem.get_items(url="https://news.ycombinator.com/"))
for item in items:
    print(item.title, item.url)
```

Run: `python demo.py`

``` shell
Notorious ‘Hijack Factory’ Shunned from Web https://krebsonsecurity.com/2018/07/notorious-hijack-factory-shunned-from-web/
 ......
```

#### Spider

For multiple pages, you can solve this with `Spider`

Create `hacker_news_spider.py`:

``` python
import aiofiles

from ruia import AttrField, TextField, Item, Spider


class HackerNewsItem(Item):
    target_item = TextField(css_select='tr.athing')
    title = TextField(css_select='a.storylink')
    url = AttrField(css_select='a.storylink', attr='href')

    async def clean_title(self, value):
        return value


class HackerNewsSpider(Spider):
    start_urls = ['https://news.ycombinator.com/news?p=1', 'https://news.ycombinator.com/news?p=2']

    async def parse(self, res):
        items = await HackerNewsItem.get_items(html=res.html)
        for item in items:
            async with aiofiles.open('./hacker_news.txt', 'a') as f:
                await f.write(item.title + '\n')


if __name__ == '__main__':
    HackerNewsSpider.start()
```

Run `hacker_news_spider.py`:

``` shell
[2018-09-21 17:27:14,497]-ruia-INFO  spider::l54: Spider started!
[2018-09-21 17:27:14,502]-Request-INFO  request::l77: <GET: https://news.ycombinator.com/news?p=2>
[2018-09-21 17:27:14,527]-Request-INFO  request::l77: <GET: https://news.ycombinator.com/news?p=1>
[2018-09-21 17:27:16,388]-ruia-INFO  spider::l122: Stopping spider: ruia
[2018-09-21 17:27:16,389]-ruia-INFO  spider::l68: Total requests: 2
[2018-09-21 17:27:16,389]-ruia-INFO  spider::l71: Time usage: 0:00:01.891688
[2018-09-21 17:27:16,389]-ruia-INFO  spider::l72: Spider finished!
```

#### Custom middleware

`ruia` provides an easy way to customize requests, *as long as it does not return it*. 

The following middleware code is based on the above example:

``` python
from ruia import Middleware

middleware = Middleware()


@middleware.request
async def print_on_request(request):
    request.metadata = {
        'index': request.url.split('=')[-1]
    }
    print(f"request: {request.metadata}")


@middleware.response
async def print_on_response(request, response):
    print(f"response: {response.metadata}")

# Add HackerNewsSpider

if __name__ == '__main__':
    HackerNewsSpider.start(middleware=middleware)
```

### Features

- Custom middleware
- JavaScript support
- Friendly response

### TODO

- [ ] Distributed crawling/scraping

### Contribution

- Pull Request
- Open Issue

### Thanks

- [sanic](https://github.com/huge-success/sanic)
- [demiurge](https://github.com/matiasb/demiurge)