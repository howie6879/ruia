#!/usr/bin/env python
"""
 Target: https://news.ycombinator.com/
 pip install aiofiles
"""
import aiofiles

from ruia import AttrField, Item, Spider, TextField


class HackerNewsItem(Item):
    target_item = TextField(css_select="tr.athing")
    title = TextField(css_select="a.storylink")
    url = AttrField(css_select="a.storylink", attr="href")

    async def clean_title(self, value):
        return value.strip()


class HackerNewsSpider(Spider):
    start_urls = [
        "https://news.ycombinator.com/news?p=1",
        "https://news.ycombinator.com/news?p=2",
    ]
    concurrency = 10
    # aiohttp_kwargs = {"proxy": "http://0.0.0.0:1087"}

    async def parse(self, response):
        async for item in HackerNewsItem.get_items(html=await response.text()):
            yield item

    async def process_item(self, item: HackerNewsItem):
        async with aiofiles.open("./hacker_news.txt", "a") as f:
            self.logger.info(item)
            await f.write(str(item.title) + "\n")


if __name__ == "__main__":
    HackerNewsSpider.start(middleware=None)
