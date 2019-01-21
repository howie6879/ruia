#!/usr/bin/env python
"""
 Target: https://news.ycombinator.com/
"""
import asyncio

from ruia import AttrField, TextField, Item


class HackerNewsItem(Item):
    target_item = TextField(css_select='tr.athing')
    title = TextField(css_select='a.storylink')
    url = AttrField(css_select='a.storylink', attr='href')

    async def clean_title(self, value):
        return value


async def single_page_demo():
    items = await HackerNewsItem.get_items(url="https://news.ycombinator.com/")
    for item in items:
        print(item.title, item.url)


async def multiple_page_demo():
    start_urls = [f'https://news.ycombinator.com/news?p={page}' for page in range(1, 3)]
    tasks = [HackerNewsItem.get_items(url=url) for url in start_urls]
    results = await asyncio.gather(*tasks)
    for items in results:
        for item in items:
            print(item.title, item.url)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(single_page_demo())
    asyncio.get_event_loop().run_until_complete(multiple_page_demo())
