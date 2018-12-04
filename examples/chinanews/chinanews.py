#!/usr/bin/env python
"""
 Created by howie.hu at 2018/9/23.
"""

from ruia import Request, Spider
from items import ChinaNewsItem
from middlewares import middleware

class ChinaNewsSpider(Spider):
    urls_db = 'mongodb://admin:11QQqqWW@192.168.99.12'
    name = 'ChinaNews'
    request_config = {
        'RETRIES': 3,
        'DELAY': 0,
        'TIMEOUT': 20
    }
    concurrency = 3

    async def parse(self, res):
        etree = res.html_etree
        urls = [i.get('href') for i in etree.cssselect('.content_list .dd_bt a')]
        for index,url in enumerate(urls):
            url = 'http:' + url
            yield Request(
                url,
                callback=self.parse_item,
                metadata={'index': index},
                request_config=self.request_config,
            )



    async def parse_item(self, res):
        print(res.url)
        item = await ChinaNewsItem.get_item(html=res.html)
        print(item.content)


if __name__ == '__main__':
    ChinaNewsSpider.start(middleware=middleware)
