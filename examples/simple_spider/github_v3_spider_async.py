# Target: https://developer.github.com/v3/
from ruia import *


class CatalogueItem(Item):
    target_item = TextField(css_select='.sidebar-menu a')
    title = TextField(css_select='a')
    link = AttrField(css_select='a', attr='href')

    async def clean_link(self, value):
        return f'https://developer.github.com{value}'


class PageItem(Item):
    content = HtmlField(css_select='.content')


class GithubDeveloperSpider(Spider):
    start_urls = ['https://developer.github.com/v3/']
    concurrency = 5

    async def parse(self, response: Response):
        catalogue = []
        async for cat in CatalogueItem.get_items(html=response.html):
            if '#' in cat.link:
                continue
            catalogue.append(cat)
        urls = [page.link for page in catalogue][:10]
        async for response in self.multiple_request(urls, is_gather=True):
            title = catalogue[response.index].title
            yield self.parse_page(response, title)

    async def parse_page(self, response, title):
        item = await PageItem.get_item(html=response.html)
        print(title, len(item.content))


class GithubDeveloperSpiderSingleRequest(Spider):
    start_urls = ['https://developer.github.com/v3/']
    concurrency = 5

    async def parse(self, response: Response):
        catalogue = []
        async for cat in CatalogueItem.get_items(html=response.html):
            if '#' in cat.link:
                continue
            catalogue.append(cat)
        for page in catalogue:
            response = await self.request(url=page.link)
            yield self.parse_page(response, page.title)

    async def parse_page(self, response, title):
        item = await PageItem.get_item(html=response.html)
        print(title, len(item.content))


if __name__ == '__main__':
    GithubDeveloperSpider.start()
