# This script is used to test some code in the topic of data cleaning.
# This script is used to test tutorials/item.md
# with using many=True parameter.

import asyncio
import os

from ruia import Item, TextField, IgnoreThisItem

HTML_PATH = os.path.join(os.path.dirname(__file__), 'item_to_ignore.html')
with open(HTML_PATH, mode="r", encoding="utf-8") as file:
    HTML = file.read()


class MyItem(Item):
    target_item = TextField(css_select='.movie')
    title = TextField(css_select=".title")
    star = TextField(css_select=".star")

    @staticmethod
    async def clean_title(value):
        if not value:
            raise IgnoreThisItem
        return value


async def main():
    items = list()
    async for item in MyItem.get_items(html=HTML):
        items.append(item)
    assert len(items) == 5


def test_main():
    asyncio.new_event_loop().run_until_complete(main())
