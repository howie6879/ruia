#!/usr/bin/env python

from ruia import AttrField, TextField, Item


class HackerNewsItem(Item):
    """
    定义目标字段抓取规则
    """
    target_item = TextField(css_select='tr.athing')
    title = TextField(css_select='a.storylink')
    url = AttrField(css_select='a.storylink', attr='href')

    async def clean_title(self, value):
        """
        清洗目标数据
        :param value: 初始目标数据
        :return:
        """
        return str(value).strip()
