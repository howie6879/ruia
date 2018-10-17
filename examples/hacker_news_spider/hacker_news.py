#!/usr/bin/env python
"""
 Created by howie.hu at 2018/9/23.
"""

from ruia import Request, Spider

from items import HackerNewsItem
from middlewares import middleware
from db import MotorBase


class HackerNewsSpider(Spider):
    start_urls = ['https://news.ycombinator.com']
    request_config = {
        'RETRIES': 3,
        'DELAY': 0,
        'TIMEOUT': 20
    }
    concurrency = 3

    async def parse(self, res):
        self.mongo_db = MotorBase().get_db('ruia_test')
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
            try:
                await self.mongo_db.news.update_one({
                    'url': item.url},
                    {'$set': {'url': item.url, 'title': item.title}},
                    upsert=True)
            except Exception as e:
                self.logger.exception(e)


if __name__ == '__main__':
    HackerNewsSpider.start(middleware=middleware)
