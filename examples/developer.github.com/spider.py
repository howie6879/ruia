# Target: https://developer.github.com/v3/
import asyncio
from ruia import *


class CatalogueItem(Item):
    target_item = TextField(css_select='.sidebar-menu a')
    title = TextField(css_select='a')
    link = AttrField(css_select='a', attr='href')

    def clean_link(self, value):
        return f'https://developer.github.com{value}'


class PageItem(Item):
    content = HtmlField(css_select='.content')


class GithubDeveloperSpider(Spider):
    start_urls = ['https://developer.github.com/v3/']
    concurrency = 5

    async def parse(self, res: Response):
        catalogue = await CatalogueItem.get_items(html=res.html)
        for page in catalogue[:20]:
            if '#' in page.link:
                continue
            yield Request(url=page.link, metadata={'title': page.title}, callback=self.parse_page)

    async def parse_page(self, res: Response):
        item = await PageItem.get_item(html=res.html)
        title = res.metadata['title']
        print(title, len(item.content))


if __name__ == '__main__':
    GithubDeveloperSpider.start()
