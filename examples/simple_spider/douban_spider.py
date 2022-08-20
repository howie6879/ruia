"""
    Created by howie.hu at 2022-08-21.
    Description: Example of Douban spider based on Ruia
    Changelog: all notable changes to this file will be documented
"""

import asyncio

from ruia import AttrField, Item, Spider, TextField


class DoubanItem(Item):
    """Define an Item for douban.com"""

    target_item = TextField(css_select="div.item")
    title = TextField(css_select="span.title")
    cover = AttrField(css_select="div.pic>a>img", attr="src")
    abstract = TextField(css_select="span.inq", default="")

    async def clean_title(self, title):
        """Clean title attr"""
        if isinstance(title, str):
            return title
        else:
            return "".join([i.text.strip().replace("\xa0", "") for i in title])


class DoubanSpider(Spider):
    """Define a Spider for douban.com"""

    name = "DoubanSpider"
    start_urls = ["https://movie.douban.com/top250"]
    request_config = {"RETRIES": 3, "DELAY": 0, "TIMEOUT": 20}
    concurrency = 10
    # aiohttp config
    aiohttp_kwargs = {}

    async def parse(self, response):
        html = await response.text()
        etree = response.html_etree(html=html)
        pages = ["?start=0&filter="] + [
            i.get("href") for i in etree.cssselect(".paginator>a")
        ]
        for index, page in enumerate(pages):
            url = self.start_urls[0] + page
            yield self.request(
                url=url, metadata={"index": index}, callback=self.parse_item
            )

    async def parse_item(self, response):
        """Parse Item"""
        async for item in DoubanItem.get_items(html=await response.text()):
            yield item

    async def process_item(self, item: DoubanItem):
        self.logger.info(item)


def multi_spider_start():
    """Start multiple crawler instances"""

    async def start():
        await asyncio.gather(
            DoubanSpider.async_start(cancel_tasks=False),
            DoubanSpider.async_start(cancel_tasks=False),
        )
        await DoubanSpider.cancel_all_tasks()

    asyncio.get_event_loop().run_until_complete(start())


if __name__ == "__main__":
    DoubanSpider.start()
    # multi_spider_start()
