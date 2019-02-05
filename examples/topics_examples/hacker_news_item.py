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
        return value.strip()


async def single_page_demo(url="https://news.ycombinator.com/"):
    async for item in HackerNewsItem.get_items(url=url):
        print(item)


async def multiple_page_demo():
    pages = [single_page_demo(f'https://news.ycombinator.com/news?p={page}') for page in range(1, 3)]
    await asyncio.gather(*pages)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(single_page_demo())
    asyncio.get_event_loop().run_until_complete(multiple_page_demo())
