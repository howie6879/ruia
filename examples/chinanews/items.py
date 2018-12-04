#!/usr/bin/env python
"""
 Created by howie.hu at 2018/9/23.
"""

from ruia import AttrField, TextField,HtmlField, Item


class ChinaNewsItem(Item):
    """
    定义目标字段抓取规则
    """
    #target_item =
    title = TextField(css_select='h1')
    content = HtmlField(css_select='div.left_zw')

    async def clean_title(self, value):
        """
        清洗目标数据
        :param value: 初始目标数据
        :return:
        """
        return value
