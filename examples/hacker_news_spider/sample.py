#!/usr/bin/env python
"""
 Created by howie.hu at 2020/12/29.
"""
from ruia import Item, Spider, TextField


class HackerNewsItem(Item):
    target_item = TextField(css_select="tr.athing")
    title = TextField(css_select="a.storylink")


class HackerNewsSpider(Spider):
    start_urls = ["https://news.ycombinator.com/news?p=1"]

    async def parse(self, response):
        async for item in HackerNewsItem.get_items(html=await response.text()):
            yield item


if __name__ == "__main__":
    HackerNewsSpider.start()
