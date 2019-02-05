# Introduction

**Ruia**是一个基于`asyncio`和`aiohttp`的异步爬虫框架，它具有编写快速，非阻塞，扩展性强等特点，
让你写更少的代码，收获更快的运行速度。

特性如下：
- 自定义中间件
- 支持js加载类型网页
- 友好地数据响应类
- 异步无阻塞

## Installation

安装**Ruia**之前请先确保你使用的是`Python3.6+`

``` shell
# For Linux & Mac
pip install -U ruia[uvloop]

# For Windows
pip install -U ruia

# New features
pip install git+https://github.com/howie6879/ruia
```

## Code Snippets

下面我将举个例子简单介绍下**Ruia**的使用方式以及框架运行流程，创建文件`hacker_news_spider.py`，然后拷贝下面代码到文件中：

```python
#!/usr/bin/env python
"""
 Target: https://news.ycombinator.com/
 pip install aiofiles
"""
import aiofiles

from ruia import AttrField, TextField, Item, Spider


class HackerNewsItem(Item):
    target_item = TextField(css_select='tr.athing')
    title = TextField(css_select='a.storylink')
    url = AttrField(css_select='a.storylink', attr='href')

    async def clean_title(self, value):
        """
        如果字段不需要清洗 这个函数可以不写
        """
        return value


class HackerNewsSpider(Spider):
    start_urls = ['https://news.ycombinator.com/news?p=1', 'https://news.ycombinator.com/news?p=2']
    concurrency = 10

    async def parse(self, response):
        async for item in HackerNewsItem.get_items(html=response.html):
            yield item

    async def process_item(self, item: HackerNewsItem):
        """Ruia build-in method"""
        async with aiofiles.open('./hacker_news.txt', 'a') as f:
            await f.write(str(item.title) + '\n')


if __name__ == '__main__':
    HackerNewsSpider.start(middleware=None)
```

在终端执行`python hacker_news_spider.py`，如果顺利的话将会得到如下输出，并且目标数据会存储在`hacker_news.txt`文件中：

```shell
[2018-09-24 11:02:05,088]-ruia-INFO  spider : Spider started!
[2018-09-24 11:02:05,089]-Request-INFO  request: <GET: https://news.ycombinator.com/news?p=2>
[2018-09-24 11:02:05,113]-Request-INFO  request: <GET: https://news.ycombinator.com/news?p=1>
[2018-09-24 11:02:09,820]-ruia-INFO  spider : Stopping spider: ruia
[2018-09-24 11:02:09,820]-ruia-INFO  spider : Total requests: 2
[2018-09-24 11:02:09,820]-ruia-INFO  spider : Time usage: 0:00:01.731780
[2018-09-24 11:02:09,821]-ruia-INFO  spider : Spider finished!
```

## Getting help

如果程序运行地不够顺利，请总结问题日志，并给我们提交[Issue](https://github.com/howie6879/ruia/issues)

恭喜你，你已经编写了一个属于自己的异步爬虫，是不是很简单，接下来你将实际编写一个例子，会更加深刻地认识到**Ruia**的强大之处，请继续阅读[Tutorials](./tutorials.md)