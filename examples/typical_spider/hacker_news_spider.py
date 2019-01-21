import asyncio
import aiofiles
from ruia import Item, TextField, AttrField, Spider


class HackerNewsItem(Item):
    target_item = TextField(css_select='tr.athing')
    title = TextField(css_select='a.storylink')
    url = AttrField(css_select='a.storylink', attr='href')


class HackerNewsSpider(Spider):
    concurrency = 2
    start_urls = [f'https://news.ycombinator.com/news?p={index}' for index in range(10)]

    async def parse(self, res):
        items = await HackerNewsItem.get_items(html=res.html)
        for item in items:
            async with aiofiles.open('./hacker_news.txt', mode='a', encoding='utf-8') as f:
                await f.write(item.title + '\n')


async def test_item():
    url = 'https://news.ycombinator.com/news?p=1'
    items = await HackerNewsItem.get_items(url=url)
    for item in items:
        print('{}: {}'.format(item.title, item.url))


if __name__ == '__main__':
    HackerNewsSpider.start()
