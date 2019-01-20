# Introduction

[![travis](https://travis-ci.org/howie6879/ruia.svg?branch=master)](https://travis-ci.org/howie6879/ruia) 
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ruia.svg)](https://pypi.org/project/ruia/) 
[![PyPI](https://img.shields.io/pypi/v/ruia.svg)](https://pypi.org/project/ruia/) 
[![license](https://img.shields.io/github/license/howie6879/ruia.svg)](https://github.com/howie6879/ruia)

![](./docs/images/demo.png)

## Overview

An async web scraping micro-framework, written with `asyncio` and `aiohttp`, 
aims to make crawling url as convenient as possible.

Write less, run faster:

- Documentation: [中文文档][doc_cn] |[documentation][doc_en]
- Plugins: [https://github.com/ruia-plugins][ruia_plugins]

## Features

- **Easy**: Declarative programming
- **Fast**: Powered by asyncio
- **Flexible**: Custom middleware
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

## Example

Let's fetch some news from [Hacker News][hacker_news] in **four** steps:

### Step 1: Define Item

After analyzing HTML structure, we define the following data item.

```python
class HackerNewsItem(ruia.Item):
    target_item = ruia.TextField(css_select='tr.athing')
    title = ruia.TextField(css_select='a.storylink')
    url = ruia.AttrField(css_select='a.storylink', attr='href')
```

### Step 2: Test Item

```python
items = HackerNewsItem.get_items(url='https://news.ycombinator.com/news?p=1')
for item in items:
    print('{}: {}'.format(item.title, item.url))

# result
# Title 1: url 1
# Title 2: url 2
# Title 3: url 3
...

```

### Step 3: Write Spider

```python
class HackerNewsSpider(ruia.Spider):
    start_urls = [
        'https://news.ycombinator.com/news?p=1',
        'https://news.ycombinator.com/news?p=2']
    
    async def parse(self, res):
        items = await HackerNewsItem.get_items(html=res.html)
        for item in items:
            async with aiofiles.open('./hacker_news.txt', 'a') as f:
                await f.write(item.title + '\n')
```

### Step 4: Run

```python
if __name__ == '__main__':
    HackerNewsSpider.start()

```
Done!

## Learn More

- [Tutorials][tutorials]
- [Topics][topics]
- [Plugins][plugins]

## TODO

- [ ] Cache for debug, to decreasing request limitation
- [ ] Distributed crawling/scraping

## Contribution

- Open Issue
- Pull Request

## Thanks

- [sanic](https://github.com/huge-success/sanic)
- [demiurge](https://github.com/matiasb/demiurge)

[doc_cn]: https://github.com/howie6879/ruia/blob/master/docs/cn/README.md
[doc_en]: https://howie6879.github.io/ruia/
[ruia_plugins]: https://github.com/ruia-plugins
[hacker_news]: https://news.ycombinator.com/news?p=1
[tutorials]: https://howie6879.github.io/ruia/en/tutorials/
[plugins]: http://howie6879.github.io/ruia/en/plugins/
[topics]: http://howie6879.github.io/ruia/en/topics/
