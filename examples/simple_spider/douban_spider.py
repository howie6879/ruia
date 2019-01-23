#!/usr/bin/env python

from ruia import AttrField, Item, Request, Spider, TextField


class DoubanItem(Item):
    target_item = TextField(css_select='div.item')
    title = TextField(css_select='span.title')
    cover = AttrField(css_select='div.pic>a>img', attr='src')
    abstract = TextField(css_select='span.inq')

    async def clean_title(self, title):
        if isinstance(title, str):
            return title
        else:
            return ''.join([i.text.strip().replace('\xa0', '') for i in title])


class DoubanSpider(Spider):
    start_urls = ['https://movie.douban.com/top250']
    request_config = {
        'RETRIES': 3,
        'DELAY': 0,
        'TIMEOUT': 20
    }
    concurrency = 10
    # proxy config
    # kwargs = {"proxy": "http://0.0.0.0:1087"}
    kwargs = {}

    async def parse(self, response):
        etree = response.html_etree
        pages = ['?start=0&filter='] + [i.get('href') for i in etree.cssselect('.paginator>a')]
        url_config_list = []
        for index, page in enumerate(pages):
            url = self.start_urls[0] + page
            url_config = {'url': url, 'metadata': {'index': index}}
            url_config_list.append(url_config)

        async for resp in self.multiple_request(url_config_list):
            yield self.parse_item(resp)

    async def parse_item(self, response):
        items_data = await DoubanItem.get_items(html=response.html)
        for item in items_data:
            print(item.title)


if __name__ == '__main__':
    DoubanSpider.start()
