#!/usr/bin/env python
"""
 pip install ruia_pyppeteer
"""

from ruia import AttrField, TextField, Item

from ruia_pyppeteer import PyppeteerSpider as Spider
from ruia_pyppeteer import PyppeteerRequest as Request


class JianshuItem(Item):
    target_item = TextField(css_select='ul.list>li')
    author_name = TextField(css_select='a.name')
    author_url = AttrField(attr='href', css_select='a.name')

    async def clean_author_url(self, author_url):
        return f"https://www.jianshu.com{author_url}"


class JianshuSpider(Spider):
    start_urls = ['https://www.jianshu.com/']
    concurrency = 10
    # Load js on the first request
    load_js = True

    async def parse(self, response):
        items = await JianshuItem.get_items(html=response.html)
        for item in items:
            print(item)
        # Loading js by using PyppeteerRequest
        yield Request(url=items[0].author_url, load_js=self.load_js, callback=self.parse_item)

    async def parse_item(self, response):
        print(response)


if __name__ == '__main__':
    JianshuSpider.start()
