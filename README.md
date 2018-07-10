## aspider

A simple,lightweight,asynchronous scraping micro-framework, written with `asyncio` and `aiohttp`.

### Installation

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


target_url = "https://news.ycombinator.com/"
loop = asyncio.get_event_loop()
items = loop.run_until_complete(HackerNewsItem.get_items(url=target_url))
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

### License
aspider is offered under the MIT license.

### Contribution

- Pull Request
- Open Issue

### Thanks

- [demiurge](https://github.com/matiasb/demiurge)