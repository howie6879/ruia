import asyncio
import sys

from ruia import Item, TextField, AttrField


class PythonDocumentationItem(Item):
    title = TextField(css_select='title')
    tutorial_link = AttrField(
        xpath_select="//a[text()='Tutorial']", attr='href')


async def field_extraction():
    url = 'https://docs.python.org/3/'
    item = await PythonDocumentationItem.get_item(url=url)
    print(item.title)
    print(item.tutorial_link)


if __name__ == '__main__':
    if sys.version_info[:2] == (3, 7):
        # Recommended for Python 3.7
        asyncio.run(field_extraction())
    else:
        loop = asyncio.new_event_loop()
        loop.run_until_complete(field_extraction())
