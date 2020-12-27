# Target: https://developer.github.com/v3/

from ruia import *

import dataset


class GithubSpiderParent(Spider):
    @classmethod
    def start(cls):
        cls.db = dataset.connect(cls.database_url)
        super().start()


class CatalogueItem(Item):
    target_item = TextField(css_select=".sidebar-menu a")
    title = TextField(css_select="a")
    link = AttrField(css_select="a", attr="href")

    async def clean_link(self, value):
        return f"https://developer.github.com{value}"


class PageItem(Item):
    content = HtmlField(css_select=".content")


class GithubDeveloperSpider(GithubSpiderParent):
    start_urls = ["https://developer.github.com/v3/"]
    concurrency = 5
    database_url = "sqlite:///developer.db"

    async def parse(self, response: Response):
        catalogue = []
        async for cat in CatalogueItem.get_items(html=await response.text()):
            if "#" in cat.link:
                continue
            catalogue.append(cat)
        urls = [page.link for page in catalogue][:10]
        async for response in self.multiple_request(urls, is_gather=True):
            title = catalogue[response.index].title
            yield self.parse_page(response, title)

    async def parse_page(self, response, title):
        item = await PageItem.get_item(html=await response.text())
        print(title, len(item.content))

        # Insert the title as a row into the database
        self.db["developers"].insert(dict(title=title))


class GithubDeveloperSpiderSingleRequest(GithubSpiderParent):
    start_urls = ["https://developer.github.com/v3/"]
    concurrency = 5
    database_url = "sqlite:///developer_single.db"

    async def parse(self, response: Response):
        catalogue = []
        async for cat in CatalogueItem.get_items(html=await response.text()):
            if "#" in cat.link:
                continue
            catalogue.append(cat)
        for page in catalogue:
            response = await self.request(url=page.link)
            yield self.parse_page(response, page.title)

    async def parse_page(self, response, title):
        item = await PageItem.get_item(html=await response.text())
        print(title, len(item.content))

        # Insert the title as a row into the database
        self.db["developer"].insert(dict(title=title))


if __name__ == "__main__":
    GithubDeveloperSpider.start()
