#!/usr/bin/env python
"""
 Created by howie.hu at 2018/9/23.
"""

from aspider import Request, Spider

from items import HackerNewsItem
from middlewares import middleware


class HackerNewsSpider(Spider):
    start_urls = ['https://news.ycombinator.com']
    concurrency = 3

    async def parse(self, res):
        urls = ['https://news.ycombinator.com/news?p=1', 'https://news.ycombinator.com/news?p=2']
        for index, url in enumerate(urls):
            yield Request(
                url,
                callback=self.parse_item,
                metadata={'index': index}
            )

    async def parse_item(self, res):
        items = await HackerNewsItem.get_items(html=res.html)
        for item in items:
            print(item.title)


if __name__ == '__main__':
    HackerNewsSpider.start(middleware=middleware)
