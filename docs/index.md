# Ruia

[![travis](https://travis-ci.org/howie6879/ruia.svg?branch=master)](https://travis-ci.org/howie6879/ruia) 
[![codecov](https://codecov.io/gh/howie6879/ruia/branch/master/graph/badge.svg)](https://codecov.io/gh/howie6879/ruia)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ruia.svg)](https://pypi.org/project/ruia/) 
[![PyPI](https://img.shields.io/pypi/v/ruia.svg)](https://pypi.org/project/ruia/) 
[![gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/howie6879_ruia/community)

![](https://raw.githubusercontent.com/howie6879/ruia/master/docs/images/ruia_demo.png)

## Overview

An async web scraping micro-framework, written with `asyncio` and `aiohttp`, 
aims to make crawling url as convenient as possible.

Write less, run faster:

- Documentation: [中文文档][doc_cn] |[documentation][doc_en]
- Awesome: [https://github.com/ruia-plugins/awesome-ruia][Awesome]
- Organization: [https://github.com/ruia-plugins][Organization]

## Features

- **Easy**: Declarative programming
- **Fast**: Powered by asyncio
- **Extensible**: Middlewares and plugins
- **Powerful**: JavaScript support

## Installation

``` shell
# For Linux & Mac
pip install -U ruia[uvloop]

# For Windows
pip install -U ruia

# New features
pip install git+https://github.com/howie6879/ruia
```

## Tutorials

1. [Overview](https://howie6879.github.io/ruia/en/tutorials/overview.html)
1. [Installation](https://howie6879.github.io/ruia/en/tutorials/installation.html)
1. [Define Data Items](https://howie6879.github.io/ruia/en/tutorials/item.html)
1. [Spider Control](https://howie6879.github.io/ruia/en/tutorials/spider.html)
1. [Request & Response](https://howie6879.github.io/ruia/en/tutorials/request.html)
1. [Customize Middleware](https://howie6879.github.io/ruia/en/tutorials/middleware.html)
1. [Write a Plugins](https://howie6879.github.io/ruia/en/tutorials/plugins.html)

## Usage

### Item

`Item` can be used standalone, for testing, and for tiny crawlers.

```python
import asyncio

from ruia import AttrField, TextField, Item


class HackerNewsItem(Item):
    target_item = TextField(css_select='tr.athing')
    title = TextField(css_select='a.storylink')
    url = AttrField(css_select='a.storylink', attr='href')

async def main():
    async for item in HackerNewsItem.get_items(url="https://news.ycombinator.com/"):
        print(item.title, item.url)

if __name__ == '__main__':
     items = asyncio.run(main())
```

Run: `python demo.py`

```shell
Notorious ‘Hijack Factory’ Shunned from Web https://krebsonsecurity.com/2018/07/notorious-hijack-factory-shunned-from-web/
 ......
```

### Spider Control

`Spider` is used for control requests better.
`Spider` supports concurrency control, which is very important for spiders.

```python
import aiofiles

from ruia import AttrField, TextField, Item, Spider


class HackerNewsItem(Item):
    target_item = TextField(css_select='tr.athing')
    title = TextField(css_select='a.storylink')
    url = AttrField(css_select='a.storylink', attr='href')

    async def clean_title(self, value):
        """Define clean_* functions for data cleaning"""
        return value.strip()


class HackerNewsSpider(Spider):
    start_urls = [f'https://news.ycombinator.com/news?p={index}' for index in range(1, 3)]

    async def parse(self, response):
        async for item in HackerNewsItem.get_items(html=response.html):
            yield item

    async def process_item(self, item: HackerNewsItem):
        """Ruia build-in method"""
        async with aiofiles.open('./hacker_news.txt', 'a') as f:
            await f.write(str(item.title) + '\n')


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

### Custom middleware

`ruia` provides an easy way to customize requests.

The following middleware is based on the above example:

```python
from ruia import Middleware

middleware = Middleware()


@middleware.request
async def print_on_request(request):
    request.metadata = {
        'index': request.url.split('=')[-1]
    }
    print(f"request: {request.metadata}")
    # Just operate request object, and do not return anything.


@middleware.response
async def print_on_response(request, response):
    print(f"response: {response.metadata}")

# Add HackerNewsSpider

if __name__ == '__main__':
    HackerNewsSpider.start(middleware=middleware)
```

### JavaScript Support

You can load js by using [ruia-pyppeteer](https://github.com/ruia-plugins/ruia-pyppeteer).

For example:

```python
import asyncio

from ruia_pyppeteer import PyppeteerRequest as Request

request = Request("https://www.jianshu.com/", load_js=True)
response = asyncio.run(request.fetch()) # Python 3.7
print(response.html)
```

## TODO

- Cache for debug, to decreasing request limitation
- Distributed crawling/scraping

## Contribution

Ruia is still under developing, feel free to open issues and pull requests:

- Report or fix bugs
- Require or publish plugins
- Write or fix documentation
- Add test cases

## Thanks

- [sanic](https://github.com/huge-success/sanic)
- [demiurge](https://github.com/matiasb/demiurge)

[doc_cn]: https://github.com/howie6879/ruia/blob/master/docs/cn/README.md
[doc_en]: https://howie6879.github.io/ruia/
[Awesome]: https://github.com/ruia-plugins/awesome-ruia
[Organization]: https://github.com/ruia-plugins
