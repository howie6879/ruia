# Python 3.7 required
import asyncio
from ruia import Item, TextField, AttrField


class HackerNewsItem(Item):
    target_item = TextField(css_select='tr.athing')
    title = TextField(css_select='a.storylink')
    url = AttrField(css_select='a.storylink', attr='href')


async def parse_one_page(page):
    url = f'https://news.ycombinator.com/news?p={page}'
    return await HackerNewsItem.get_items(url=url)


async def main():
    coroutine_list = [parse_one_page(page) for page in range(1, 3)]
    result = await asyncio.gather(*coroutine_list)
    news_list = list()
    for one_page_list in result:
        news_list.extend(one_page_list)
    for news in news_list:
        print(news.title, news.url)


if __name__ == '__main__':
    asyncio.run(main())
