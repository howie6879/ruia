#!/usr/bin/env python
"""
 Created by howie.hu at 2018/9/23.
"""

from aspider import AttrField, TextField, Item


class HackerNewsItem(Item):
    target_item = TextField(css_select='tr.athing')
    title = TextField(css_select='a.storylink')
    url = AttrField(css_select='a.storylink', attr='href')

    async def clean_title(self, value):
        return value
