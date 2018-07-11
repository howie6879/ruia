## aspider

A lightweight,asynchronous,distributed scraping micro-framework, written with `asyncio` and `aiohttp`.

- Python versions: 3.6+
- Free software: MIT license

### Installation

``` shell
pip install git+https://github.com/howie6879/aspider
```

### Usage

#### Item

Let's take a look at a quick example of using `Item`. Start off by adding the following to your demo.py:

``` python
import asyncio

from pprint import pprint

from aspider import AttrField, TextField, Item


class HackerNewsItem(Item):
    target_item = TextField(css_select='tr.athing')
    title = TextField(css_select='a.storylink')
    url = AttrField(css_select='a.storylink', attr='href')


items = asyncio.get_event_loop().run_until_complete(HackerNewsItem.get_items(url="https://news.ycombinator.com/"))
pprint(items)

```

Run: `python demo.py`

``` shell
[2018-07-10 16:07:02,831]-Request-INFO  <GET: https://news.ycombinator.com/>
[{'title': 'Show HN: Browsh – A modern, text-based browser',
  'url': 'https://www.brow.sh'},
 {'title': 'The Effects of CPU Turbo: 768X Stddev',
  'url': 'https://www.alexgallego.org/perf/compiler/explorer/flatbuffers/smf/2018/06/30/effects-cpu-turbo.html'},
 {'title': 'What industry has the highest revenue per employee?',
  'url': 'https://craft.co/reports/where-do-the-most-productive-employees-work'},
 {'title': 'The 111M Record Pemiblanc Credential Stuffing List',
  'url': 'https://www.troyhunt.com/the-111-million-pemiblanc-credential-stuffing-list/'},
 {'title': 'How to Analyze Billions of Records per Second on a Single Desktop '
           'PC',
 ......
```

#### Spider

For multiple pages, you can solve this with `Spider`

Create `hacker_news_spider.py`:

``` python
import aiofiles

from aspider import AttrField, TextField, Item, Spider


class HackerNewsItem(Item):
    target_item = TextField(css_select='tr.athing')
    title = TextField(css_select='a.storylink')
    url = AttrField(css_select='a.storylink', attr='href')

    async def clean_title(self, value):
        return value


class HackerNewsSpider(Spider):
    start_urls = ['https://news.ycombinator.com/', 'https://news.ycombinator.com/news?p=2']

    async def parse(self, res):
        items = await HackerNewsItem.get_items(html=res.html)
        for item in items:
            async with aiofiles.open('./hacker_news.txt', 'a') as f:
                await f.write(item['title'] + '\n')


if __name__ == '__main__':
    HackerNewsSpider.start()
```

Run `hacker_news_spider.py`:

``` shell
[2018-07-11 17:50:12,430]-aspider-INFO  Spider started!
[2018-07-11 17:50:12,430]-Request-INFO  <GET: https://news.ycombinator.com/>
[2018-07-11 17:50:12,456]-Request-INFO  <GET: https://news.ycombinator.com/news?p=2>
[2018-07-11 17:50:14,785]-aspider-INFO  Time usage: 0:00:02.355062
[2018-07-11 17:50:14,785]-aspider-INFO  Spider finished!
```

#### Distributed scraping - TODO

### Contribution

- Pull Request
- Open Issue

### Thanks

- [demiurge](https://github.com/matiasb/demiurge)