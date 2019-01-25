from ruia import TextField, Item, Spider


class HackerNewsItem(Item):
    target_item = TextField(css_select='tr.athing')
    title = TextField(css_select='a.storylink')


class HackerNewsSpider(Spider):
    start_urls = ['https://news.ycombinator.com/news?p=1']

    async def parse(self, response):
        async for item in HackerNewsItem.get_items(html=response.html):
            yield item

    async def save_item(self, item: HackerNewsItem):
        # process item result data
        pass


if __name__ == '__main__':
    HackerNewsSpider.start()
