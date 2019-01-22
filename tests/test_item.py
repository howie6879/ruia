#!/usr/bin/env python

import asyncio
import os

import pytest

from ruia import AttrField, Item, TextField

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


def test_item():
    item = asyncio.get_event_loop().run_until_complete(DoubanItem.get_item(html=HTML))
    assert item.title == 'Title: 豆瓣电影TOP250'


def test_items():
    items = asyncio.get_event_loop().run_until_complete(DoubanItems.get_items(html=HTML))
    print(items[0].results)
    assert items[0].abstract == '希望让人自由。'


def test_item_results():
    item = asyncio.get_event_loop().run_until_complete(DoubanItem.get_item(html=HTML))
    assert item.results == {'title': 'Title: 豆瓣电影TOP250'}


def test_items_results():
    items = asyncio.get_event_loop().run_until_complete(DoubanItems.get_items(html=HTML))
    assert items[0].results['title'] == '肖申克的救赎'
