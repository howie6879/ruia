# Create A Parent Class For Your Spiders

## A Simple Example

Take following basic spiders:

```python
# Target: https://developer.github.com/v3/
from ruia import *


class CatalogueItem(Item):
    target_item = TextField(css_select=".sidebar-menu a")
    title = TextField(css_select="a")
    link = AttrField(css_select="a", attr="href")

    async def clean_link(self, value):
        return f"https://developer.github.com{value}"


class PageItem(Item):
    content = HtmlField(css_select=".content")


class GithubDeveloperSpider(Spider):
    start_urls = ["https://developer.github.com/v3/"]
    concurrency = 5

    async def parse(self, response: Response):
        catalogue = []
        async for cat in CatalogueItem.get_items(html=response.html):
            if "#" in cat.link:
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
    start_urls = ["https://developer.github.com/v3/"]
    concurrency = 5

    async def parse(self, response: Response):
        catalogue = []
        async for cat in CatalogueItem.get_items(html=response.html):
            if "#" in cat.link:
                continue
            catalogue.append(cat)
        for page in catalogue:
            response = await self.request(url=page.link)
            yield self.parse_page(response, page.title)

    async def parse_page(self, response, title):
        item = await PageItem.get_item(html=response.html)
        print(title, len(item.content))


if __name__ == "__main__":
    GithubDeveloperSpider.start()

```

As you can see, there is quite a bit of common code in all the spiders - for example the `start_urls` and `concurrency` variables as they are standard in this project, and, of particular interest, the `parse_page` function. We'd like to refactor the commonalities into a parent class. To do this is very easy - we define the parent class with the common variables/functions contained:

```python
class GithubSpiderParent(Spider):
    start_urls = ["https://developer.github.com/v3/"]
    concurrency = 5

    async def parse_page(self, response, title):
        item = await PageItem.get_item(html=response.html)
        print(title, len(item.content))
```

And then we can refactor the two spiders:

```python
class GithubDeveloperSpider(Spider):
    async def parse(self, response: Response):
        catalogue = []
        async for cat in CatalogueItem.get_items(html=response.html):
            if "#" in cat.link:
                continue
            catalogue.append(cat)
        urls = [page.link for page in catalogue][:10]
        async for response in self.multiple_request(urls, is_gather=True):
            title = catalogue[response.index].title
            yield self.parse_page(response, title)


class GithubDeveloperSpiderSingleRequest(Spider):
    async def parse(self, response: Response):
        catalogue = []
        async for cat in CatalogueItem.get_items(html=response.html):
            if "#" in cat.link:
                continue
            catalogue.append(cat)
        for page in catalogue:
            response = await self.request(url=page.link)
            yield self.parse_page(response, page.title)
```

## A More Complex Example

Say you wanted to dynamically initialise objects for the `Spider` sub-classes, e.g. a unique database connection for each class in which the data the spiders retrieve is inserted into. There are a few ways to go about doing this, but the most concise is to use a parent class, as above, with a few modifications. First let us define the database connection strings in the spiders. This tutorial assumes that the `dataset` (https://dataset.readthedocs.io/en/latest/) library is pre-installed:

```python
class GithubDeveloperSpider(GithubSpiderParent):
    start_urls = ["https://developer.github.com/v3/"]
    concurrency = 5
    database_url = "sqlite:///developer.db"

    async def parse(self, response: Response):
        catalogue = []
        async for cat in CatalogueItem.get_items(html=response.html):
            if "#" in cat.link:
                continue
            catalogue.append(cat)
        urls = [page.link for page in catalogue][:10]
        async for response in self.multiple_request(urls, is_gather=True):
            title = catalogue[response.index].title
            yield self.parse_page(response, title)

    async def parse_page(self, response, title):
        item = await PageItem.get_item(html=response.html)
        print(title, len(item.content))

        # Insert the title as a row into the database
        self.db['developers'].insert(dict(title=title))


class GithubDeveloperSpiderSingleRequest(GithubSpiderParent):
    start_urls = ["https://developer.github.com/v3/"]
    concurrency = 5
    database_url = "sqlite:///developer_single.db"

    async def parse(self, response: Response):
        catalogue = []
        async for cat in CatalogueItem.get_items(html=response.html):
            if "#" in cat.link:
                continue
            catalogue.append(cat)
        for page in catalogue:
            response = await self.request(url=page.link)
            yield self.parse_page(response, page.title)

    async def parse_page(self, response, title):
        item = await PageItem.get_item(html=response.html)
        print(title, len(item.content))

        # Insert the title as a row into the database
        self.db['developer'].insert(dict(title=title))
```

Now you may assume that the parent class for creating a database connection at initialisation would be something like this:

```
import dataset


class GithubSpiderParent(Spider):
    def __init__(self, *args, **kwargs):
        super(Spider, self).__init__(*args, **kwargs)
        self.db = dataset.connect(self.database_url)
```

But this is incorrect. Why? Because of `classmethods`. It can be a slightly difficult concept to grasp - `classmethods` give you control of the class at a class level, not at an instance level (as `self` does) and therefore you must attach the database connection to the class instance. Thus to acheive the aforementioned goal the parent class needs to be so:

```
import dataset


class GithubSpiderParent(Spider):
    @classmethod
    def start(cls):
        cls.db = dataset.connect(cls.database_url)
        super().start()
```

And you should a `developer.db` should be created.
