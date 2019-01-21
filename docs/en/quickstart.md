# Create a Typical Ruia Spider

Let's fetch some news from [Hacker News][hacker_news] in **four** steps:

- Define item
- Test item
- Write spider
- Run

## Step 1: Define Item

After analyzing HTML structure, we define the following data item.

The skill of analyzing HTML structure is important for a spider engineer,
`Ruia` believe you have already had this skill,
and won't talk about it here.


```python
from ruia import Item, TextField, AttrField


class HackerNewsItem(Item):
    target_item = TextField(css_select='tr.athing')
    title = TextField(css_select='a.storylink')
    url = AttrField(css_select='a.storylink', attr='href')
    
```

It's easy to understand:
we want to get an item from HTML structure,
the item contains two fields: `title` and `url`.

Wait! What is `target_item`?

`target_item` is a built-in `Ruia field`,
indicates that the HTML element matched by its selectors contains one item.
In this example, we are crawling a catalogue of Hacker News,
and there are many news items in one page. 
`target_item` tells `Ruia` to focus on these HTML elements when extracting field.

## Step 2: Test Item

Ruia is a low-coupling spider frame.
Each class can be used separately in your project.
You can even write a [simple spider](examples/simple.md) with only `ruia.Item`,`ruia.TextField` and `ruia.AttrField`.
This feature provides a convenient way to test `HackerNewsItem`.

```python
import asyncio

from ruia import Item, TextField, AttrField


class HackerNewsItem(Item):
    target_item = TextField(css_select='tr.athing')
    title = TextField(css_select='a.storylink')
    url = AttrField(css_select='a.storylink', attr='href')


async def test_item():
    url = 'https://news.ycombinator.com/news?p=1'
    items = await HackerNewsItem.get_items(url=url)
    for item in items:
        print('{}: {}'.format(item.title, item.url))


if __name__ == '__main__':
    asyncio.run(test_item()) # Python 3.7 Required.

    # For Python 3.6
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(test_item())

```

Waiting for the output in your console.

## Step 3: Write Spider

In the example [quick start](examples/simple.md),
we talk about such an pity,
that the simple spider do not have a concurrency control.
It's important for a spider,
or you will be banned by the server in one minute.

`ruia.Spider` aims at solving this problem,
by default, the concurrency is 3.

```python
import aiofiles

from ruia import Item, TextField, AttrField, Spider


class HackerNewsItem(Item):
    target_item = TextField(css_select='tr.athing')
    title = TextField(css_select='a.storylink')
    url = AttrField(css_select='a.storylink', attr='href')


class HackerNewsSpider(Spider):
    concurrency = 2
    start_urls = [f'https://news.ycombinator.com/news?p={index}' for index in range(3)]

    async def parse(self, res):
        items = await HackerNewsItem.get_items(html=res.html)
        for item in items:
            async with aiofiles.open('./hacker_news.txt', mode='a', encoding='utf-8') as f:
                await f.write(item.title + '\n')

```

Just define a property of the subclass of `Spider`.
In this example, we crawl in two coroutines.
If you do not know coroutine,
as a crawler engineer,
`ruia` believe you know the threading pool of spider.
Coroutine is a more efficient way to behave like threading pool.

`parse(self, response)` is the **entry point** of a spider.
After starting a spider, it send requests to web server.
Once received a response, 
`ruia.Spider` will call its `parse` function to extract data from HTML source code.

## Step 4: Run

Now everything is ready.
Run!

```python
import aiofiles

from ruia import Item, TextField, AttrField, Spider


class HackerNewsItem(Item):
    target_item = TextField(css_select='tr.athing')
    title = TextField(css_select='a.storylink')
    url = AttrField(css_select='a.storylink', attr='href')


class HackerNewsSpider(Spider):
    concurrency = 2
    start_urls = [f'https://news.ycombinator.com/news?p={index}' for index in range(3)]

    async def parse(self, res):
        items = await HackerNewsItem.get_items(html=res.html)
        for item in items:
            async with aiofiles.open('./hacker_news.txt', mode='a', encoding='utf-8') as f:
                await f.write(item.title + '\n')


if __name__ == '__main__':
    HackerNewsSpider.start()
```

Hey, notice that, do not run `Spider.start()` in a `await` statement!
It's just a **normal function**!

You just create a spider in one python file!
Amazing!

[hacker_news]: https://news.ycombinator.com/news?p=1