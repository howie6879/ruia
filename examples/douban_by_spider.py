#!/usr/bin/env python
"""
 Created by howie.hu at 2018/7/12.
"""
from aspider import AttrField, TextField, Item, Request, Spider
from aspider.utils import get_random_user_agent


class DoubanItem(Item):
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
    start_urls = ['https://movie.douban.com/top250']
    request_config = {
        'RETRIES': 3,
        'DELAY': 0,
        'TIMEOUT': 20
    }

    async def parse(self, res):
        etree = res.e_html
        pages = [i.get('href') for i in etree.cssselect('.paginator>a')]
        pages.insert(0, '?start=0&filter=')
        headers = {
            "User-Agent": await get_random_user_agent()
        }
        for page in pages:
            url = self.start_urls[0] + page
            yield Request(url, request_config=self.request_config, headers=headers, callback=self.parse_item)

    async def parse_item(self, res):
        items_data = await DoubanItem.get_items(html=res.html)
        for item in items_data:
            print(item.title)


if __name__ == '__main__':
    DoubanSpider.start()
