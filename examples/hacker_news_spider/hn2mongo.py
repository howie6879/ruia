#!/usr/bin/env python
"""
 Created by howie.hu at 2021/4/4.
"""
from ruia_motor import RuiaMotorInsert, init_spider

from ruia import AttrField, Item, Spider, TextField


class HackerNewsItem(Item):
    target_item = TextField(css_select="tr.athing")
    title = TextField(css_select="a.storylink")
    url = AttrField(css_select="a.storylink", attr="href")


class HackerNewsSpider(Spider):
    start_urls = [f"https://news.ycombinator.com/news?p={index}" for index in range(3)]
    concurrency = 3

    # 设置代理
    aiohttp_kwargs = {"proxy": "http://0.0.0.0:1087"}

    async def parse(self, response):
        async for item in HackerNewsItem.get_items(html=await response.text()):
            yield RuiaMotorInsert(collection="news", data=item.results)


async def init_plugins_after_start(spider_ins):
    spider_ins.mongodb_config = {"host": "127.0.0.1", "port": 27017, "db": "ruia_motor"}
    init_spider(spider_ins=spider_ins)


if __name__ == "__main__":
    HackerNewsSpider.start(after_start=init_plugins_after_start)
