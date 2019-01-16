import asyncio
from ruia import Item, TextField, AttrField


class GithiubIssueItem(Item):
    title = TextField(css_select='title')
    tags = AttrField(css_select='a.IssueLabel', attr='data-name', many=True)


item = asyncio.run(GithiubIssueItem.get_item(url='https://github.com/pypa/pip/issues/72'))
assert isinstance(item.tags, list)
