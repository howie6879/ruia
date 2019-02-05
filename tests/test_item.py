#!/usr/bin/env python

import asyncio
import os

from ruia import AttrField, Item, TextField
from ruia.exceptions import InvalidFuncType

html_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data', 'for_item_testing.html')
with open(html_path, mode='r', encoding='utf-8') as file:
    HTML = file.read()


class DoubanItems(Item):
    target_item = TextField(css_select='div.item')
    title = TextField(css_select='span.title')
    cover = AttrField(css_select='div.pic>a>img', attr='src')
    abstract = TextField(css_select='span.inq')

    async def clean_title(self, title):
        if isinstance(title, str):
            return title
        else:
            return ''.join([i.text.strip().replace('\xa0', '') for i in title])


class DoubanItem(Item):
    title = TextField(css_select='head title')

    async def clean_title(self, title):
        return 'Title: ' + title


class DoubanCleanMethodErrorItem(Item):
    title = TextField(css_select='head title')

    def clean_title(self, title):
        return 'Title: ' + title


class HackerNewsItem(Item):
    target_item = TextField(css_select='tr.athing')
    title = TextField(css_select='a.storylink')
    url = AttrField(css_select='a.storylink', attr='href')


async def parse_item(html):
    items = []
    async for item in DoubanItems.get_items(html=html):
        items.append(item)
    return items


async def error_parse_item(html):
    items = []
    async for item in DoubanItem.get_items(html=html):
        items.append(item)
    return items


async def single_page_demo(url="https://news.ycombinator.com/"):
    items = []
    async for item in HackerNewsItem.get_items(url=url, sem=asyncio.Semaphore(3)):
        items.append(item)
    return items


def test_item():
    item = asyncio.get_event_loop().run_until_complete(DoubanItem.get_item(html=HTML))
    assert item.title == 'Title: 豆瓣电影TOP250'

    try:
        item = asyncio.get_event_loop().run_until_complete(DoubanCleanMethodErrorItem.get_item(html=HTML))
    except Exception as e:
        assert isinstance(e, InvalidFuncType)

    try:

        item = asyncio.get_event_loop().run_until_complete(DoubanItem.get_item(html=''))
    except Exception as e:
        assert isinstance(e, ValueError)

    try:
        item = asyncio.get_event_loop().run_until_complete(DoubanItem.get_item(html_etree='test'))
    except Exception as e:
        assert isinstance(e, AttributeError)


def test_items():
    items = asyncio.get_event_loop().run_until_complete(parse_item(html=HTML))
    assert items[0].abstract == '希望让人自由。'

    try:
        items = asyncio.get_event_loop().run_until_complete(error_parse_item(html=HTML))
    except Exception as e:
        assert isinstance(e, ValueError)


def test_item_results():
    item = asyncio.get_event_loop().run_until_complete(DoubanItem.get_item(html=HTML))
    assert item.results == {'title': 'Title: 豆瓣电影TOP250'}


def test_items_results():
    items = asyncio.get_event_loop().run_until_complete(parse_item(html=HTML))
    assert items[0].results['title'] == '肖申克的救赎'


def test_request_url():
    items = asyncio.get_event_loop().run_until_complete(single_page_demo())
    assert isinstance(items, list)
    assert len(items) > 1
    assert 'Item' in str(items[0])
