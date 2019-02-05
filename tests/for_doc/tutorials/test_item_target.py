# This script is used to test tutorials/item.md
# with using target_item field.


import asyncio
import os
import sys

from ruia import Item, TextField

with open(os.path.join(os.path.dirname(__file__), 'target_item.html'), mode='r', encoding='utf-8') as file:
    HTML = file.read()


class MyItem(Item):
    target_item = TextField(css_select='.movie')
    title = TextField(css_select='.title')
    star = TextField(css_select='.star')

    async def clean_star(self, value):
        return int(value)


async def main():
    async for item in MyItem.get_items(html=HTML):
        print(f'Title={item.title}, Star={item.star}')


def test_main():
    if sys.version_info[:2] == (3, 7):
        # Recommended for Python 3.7
        asyncio.run(main())
    else:
        loop = asyncio.new_event_loop()
        loop.run_until_complete(main())
