# This script is used to test tutorials/item.md
# with using many=True parameter.


import os
import asyncio
from ruia import Item, AttrField, TextField

with open(os.path.join(os.path.dirname(__file__), 'many_parameter.html'), mode='r', encoding='utf-8') as file:
    HTML = file.read()


class MyItem(Item):
    title = TextField(css_select='.title')
    star = TextField(css_select='.star')
    tags = TextField(css_select='.tag', many=True)

    def clean_star(self, value):
        return int(value)


async def main():
    item = await MyItem.get_item(html=HTML)
    print('Title: ', item.title)
    print('Star: ', item.star)
    for tag in item.tags:
        print('Tag: ', tag)


def test_main():
    asyncio.run(main())  # Python 3.7 required

    # For python 3.6
    # loop = asyncio.new_event_loop()
    # loop.run_until_complete(main())
