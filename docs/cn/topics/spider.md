# Spider

`Spider`是爬虫程序的入口，它将Item、Middleware、Request、等模块组合在一起，从而为你构造一个稳健的爬虫程序。你只需要关注以下两个函数：
- [Spider.start]()：爬虫的启动函数
- [parse]()：爬虫的第一层解析函数，继承`Spider`的子类必须实现这个函数

## Core arguments

`Spider.start`的参数如下：
- after_start：爬虫启动后的钩子函数
- before_stop：爬虫启动前的钩子函数
- middleware：中间件类，可以是一个中间件`Middleware()`实例，也可以是一组`Middleware()`实例组成的列表
- loop：事件循环

## Usage

```python
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

## How It Works?
`Spider`会自动读取`start_urls`列表里面的请求链接，然后维护一个异步队列，使用生产消费者模式进行爬取，爬虫程序一直循环直到没有调用函数为止