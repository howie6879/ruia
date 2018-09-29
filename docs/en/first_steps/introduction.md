## Introduction

**aspider** is an asynchronous crawler framework, based on `asyncio` and `aiohttp`. *Write less, run faster* is aspider's philosophy.

**Fetures**

- Asynchronous
- Custom Middleware
- JavaScript Parsing
- Friendly Response Classes

### Installation

The first step is make sure that you are using `Python3.6+`, then run the following commands

```shell
# For Linux & Mac
$ pip install -U aspider[uvloop]

# For Windows
$ pip install -U aspider

# New features
$ pip install git+https://github.com/howie6879/aspider
```

### Example

Here's a simple crawler to learn aspider. First, create a file and name it `hacker_news_spider.py`, then copy and paste the following code

```python
#!/usr/bin/env python
"""
 Target: https://news.ycombinator.com/
 pip install aiofiles
"""
import aiofiles

from aspider import AttrField, TextField, Item, Spider


class HackerNewsItem(Item):
    target_item = TextField(css_select='tr.athing')
    title = TextField(css_select='a.storylink')
    url = AttrField(css_select='a.storylink', attr='href')

    async def clean_title(self, value):
        return value


class HackerNewsSpider(Spider):
    start_urls = ['https://news.ycombinator.com/news?p=1', 'https://news.ycombinator.com/news?p=2']
    concurrency = 10

    async def parse(self, res):
        items = await HackerNewsItem.get_items(html=res.html)
        for item in items:
            async with aiofiles.open('./hacker_news.txt', 'a') as f:
                await f.write(item.title + '\n')


if __name__ == '__main__':
    HackerNewsSpider.start(middleware=None)
```

Done! Let's run this script in terminal `python hacker_news_spider.py`, if it works, you'll see something like

```
[2018-09-24 11:02:05,088]-aspider-INFO  spider : Spider started!
[2018-09-24 11:02:05,089]-Request-INFO  request: <GET: https://news.ycombinator.com/news?p=2>
[2018-09-24 11:02:05,113]-Request-INFO  request: <GET: https://news.ycombinator.com/news?p=1>
[2018-09-24 11:02:09,820]-aspider-INFO  spider : Stopping spider: aspider
[2018-09-24 11:02:09,820]-aspider-INFO  spider : Total requests: 2
[2018-09-24 11:02:09,820]-aspider-INFO  spider : Time usage: 0:00:01.731780
[2018-09-24 11:02:09,821]-aspider-INFO  spider : Spider finished!
```

Besides, you can find a file `hacker_news.txt` in the working directory, stored the target data.

Congrats🎉, you finished your first crawler by using aspider, wanna learn more? [Tutorials](./tutorials.md) are available!

### FAQ & Feedback

Need some help? Should there be any questions, don't hesitate to create [issuses](https://github.com/howie6879/aspider/issues).

