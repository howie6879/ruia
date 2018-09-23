## Introduction

[![travis](https://travis-ci.org/howie6879/aspider.svg?branch=master)](https://travis-ci.org/howie6879/aspider) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/aspider.svg)](https://pypi.org/project/aspider/) [![PyPI](https://img.shields.io/pypi/v/aspider.svg)](https://pypi.org/project/aspider/) [![license](https://img.shields.io/github/license/howie6879/aspider.svg)](https://github.com/howie6879/aspider)


**aspider**是一个基于`asyncio`和`aiohttp`的异步爬虫框架，它具有编写快速，非阻塞，扩展性强等特点，让你写更少的代码，收获更快的运行速度

特性如下：
- 自定义中间件
- 支持js加载类型网页
- 友好地数据响应类
- 异步无阻塞

### Installation

安装**aspider**之前请先确保你使用的是`Python3.6+`

``` shell
# For Linux & Mac
pip install -U aspider[uvloop]

# For Windows
pip install -U aspider

# New features
pip install git+https://github.com/howie6879/aspider
```

### Code Snippets

下面我将举个例子简单介绍下**aspider**的使用方式以及框架运行流程，创建文件`douban_spider.py`，然后拷贝下面代码到文件中：

```python
from aspider import AttrField, TextField, Item, Request, Spider


class DoubanItem(Item):
    """
    定义爬虫的目标字段
    """
    target_item = TextField(css_select='div.item')
    title = TextField(css_select='span.title')
    cover = AttrField(css_select='div.pic>a>img', attr='src')
    abstract = TextField(css_select='span.inq')

    async def clean_title(self, title):
        if isinstance(title, str):
            return title
        else:
            return ''.join([i.text.strip().replace('\xa0', '') for i in title])


class DoubanSpider(Spider):
    """
    爬虫程序的入口
    """
    start_urls = ['https://movie.douban.com/top250']
    request_config = {
        'RETRIES': 3,
        'DELAY': 0,
        'TIMEOUT': 20
    }
    concurrency = 10

    async def parse(self, res):
        etree = res.e_html
        pages = ['?start=0&filter='] + [i.get('href') for i in etree.cssselect('.paginator>a')]
        for index, page in enumerate(pages):
            url = self.start_urls[0] + page
            yield Request(
                url,
                callback=self.parse_item,
                metadata={'index': index},
                request_config=self.request_config
            )

    async def parse_item(self, res):
        items_data = await DoubanItem.get_items(html=res.html)
        title_list = []
        for item in items_data:
            title_list.append(item.title)
        return title_list


if __name__ == '__main__':
    DoubanSpider.start()
```

在终端执行`python douban_spider.py`，如果顺利的话将会得到如下输出：

```shell
[2018-09-23 23:13:09,220]-aspider-INFO  spider : Spider started!
[2018-09-23 23:13:09,221]-Request-INFO  request: <GET: https://movie.douban.com/top250>
[2018-09-23 23:13:09,633]-Request-INFO  request: <GET: https://movie.douban.com/top250?start=225&filter=>
[2018-09-23 23:13:09,634]-Request-INFO  request: <GET: https://movie.douban.com/top250?start=100&filter=>
[2018-09-23 23:13:09,635]-Request-INFO  request: <GET: https://movie.douban.com/top250?start=125&filter=>
[2018-09-23 23:13:09,635]-Request-INFO  request: <GET: https://movie.douban.com/top250?start=0&filter=>
[2018-09-23 23:13:09,636]-Request-INFO  request: <GET: https://movie.douban.com/top250?start=150&filter=>
[2018-09-23 23:13:09,636]-Request-INFO  request: <GET: https://movie.douban.com/top250?start=25&filter=>
[2018-09-23 23:13:09,637]-Request-INFO  request: <GET: https://movie.douban.com/top250?start=175&filter=>
[2018-09-23 23:13:09,638]-Request-INFO  request: <GET: https://movie.douban.com/top250?start=50&filter=>
[2018-09-23 23:13:09,638]-Request-INFO  request: <GET: https://movie.douban.com/top250?start=200&filter=>
[2018-09-23 23:13:09,639]-Request-INFO  request: <GET: https://movie.douban.com/top250?start=75&filter=>
[2018-09-23 23:13:10,198]-aspider-INFO  spider : Stopping spider: aspider
[2018-09-23 23:13:10,199]-aspider-INFO  spider : Total requests: 11
[2018-09-23 23:13:10,199]-aspider-INFO  spider : Time usage: 0:00:00.978793
[2018-09-23 23:13:10,199]-aspider-INFO  spider : Spider finished!
```

### Getting help

如果程序运行地不够顺利，请总结问题日志，并给我们提交[Issue](https://github.com/howie6879/aspider/issues)

恭喜你，你已经编写了一个属于自己的异步爬虫，是不是很简单，接下来你将实际编写一个例子，会更加深刻地认识到**aspider**的强大之处，请继续阅读[tutorials](./tutorials.md)