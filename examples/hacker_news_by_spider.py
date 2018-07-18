#!/usr/bin/env python
"""
 Target: https://news.ycombinator.com/
"""
import aiofiles

from aspider import AttrField, TextField, Item, Spider


class HackerNewsItem(Item):
    target_item = TextField(css_select='tr.athing')
    title = TextField(css_select='a.storylink')
    url = AttrField(css_select='a.storylink', attr='href')

    async def clean_title(self, value):
        return value


class HackerNewsSpider(Spider):
    start_urls = ['https://news.ycombinator.com/', 'https://news.ycombinator.com/news?p=2']

    async def parse(self, res):
        items = await HackerNewsItem.get_items(html=res.html)
        for item in items:
            async with aiofiles.open('./hacker_news.txt', 'a') as f:
                await f.write(item.title + '\n')


if __name__ == '__main__':
    HackerNewsSpider.start()
