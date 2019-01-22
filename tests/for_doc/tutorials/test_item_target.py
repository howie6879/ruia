# This script is used to test tutorials/item.md
# with using target_item field.


import os
import asyncio
from ruia import Item, AttrField, TextField

with open(os.path.join(os.path.dirname(__file__), 'target_item.html'), mode='r', encoding='utf-8') as file:
    HTML = file.read()


class MyItem(Item):
    target_item = TextField(css_select='.movie')
    title = TextField(css_select='.title')
    star = TextField(css_select='.star')

    def clean_star(self, value):
        return int(value)


async def main():
    items = await MyItem.get_items(html=HTML)
    for item in items:
        print(f'Title={item.title}, Star={item.star}')


def test_main():
    asyncio.run(main())  # Python 3.7 required

    # For python 3.6
    # loop = asyncio.new_event_loop()
    # loop.run_until_complete(main())
