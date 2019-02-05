# Write Spiders like Scrapy

I am a user of scrapy myself.
Scrapy is a great framework, which is a de facto standard of python crawlers for years.

Ruia provides APIs like scrapy,
for users to migrate crawlers from scrapy to ruia.
If you like the Declarative Programming feature,
but you know little about python async/await syntax,
this essay is for you.

For this example, we'll crawl [Github Developer Documentation](https://developer.github.com/v3/).

```python
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

    async def parse(self, response: Response):
        catalogue = []
        async for cat in CatalogueItem.get_items(html=response.html):
            catalogue.append(cat)
        for page in catalogue[:6]:
            if '#' in page.link:
                continue
            yield Request(url=page.link, metadata={'title': page.title}, callback=self.parse_page)

    async def parse_page(self, response: Response):
        item = await PageItem.get_item(html=response.html)
        title = response.metadata['title']
        print(title, len(item.content))
```

See the `GithubDeveloperSpider.parse` method.
After extracting titles and urls,
it `yield` a request.

About `yield`,
you should learn from python documentation.
Here we can regard it as sending a task to background process.

Okay, now that we have already send the request to background process,
we have loss the control of the request.
Nothing serious,
after the request finished,
the response will send to its `callback` parameter.
`callback` parameter should be a function, or something callable.
In `parse_page` method,
we accept the response.
Then it comes with another problem:
we have already get the page title from catalogue in method `parse`,
but they are not in the context of `parse_page`.
That's why we need a `metadata` argument.
we put data into `metadata` in the previous method,
and get data from it in the following method.

Now, run the spider.

```text
output:
Media Types 8652
Overview 38490
OAuth Authorizations API 66565
Other Authentication Methods 6651
Troubleshooting 2551
```

BTW, we sincerely recommend you to migrate your code to new APIs of `ruia`.
`ruia` provides a better way to replace callback functions with coroutines.
It provides more readability and is more flexible.
We do not need callback and metadata now.
Crawlers are more concise.
