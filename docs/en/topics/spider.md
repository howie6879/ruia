## Spider

`Spider` is the entrypoint of the crawler program.
It combines `Item`, `Middleware`, `Request` and other models, to build a strong crawler for you.
You should focus on the following two functions:

- Spider.start(): the entrypoint
- parse(): The first parse function, required for subclass of `Spider`

### Core arguments

`Spider.start` arguments:

- after_start: a hook after starting the crawler
- before_stop: a hook before starting the crawler
- middleware: `Middleware` class, can be an object of `Middleware()`, or a list of `Middleware()`
- loop: event loop

### Usage

```python
import aiofiles

from ruia import AttrField, TextField, Item, Spider


class HackerNewsItem(Item):
    target_item = TextField(css_select='tr.athing')
    title = TextField(css_select='a.storylink')
    url = AttrField(css_select='a.storylink', attr='href')

    async def clean_title(self, value):
        return value


class HackerNewsSpider(Spider):
    start_urls = ['https://news.ycombinator.com/news?p=1', 'https://news.ycombinator.com/news?p=2']

    async def parse(self, res):
        items = await HackerNewsItem.get_items(html=res.html)
        for item in items:
            async with aiofiles.open('./hacker_news.txt', 'a') as f:
                await f.write(item.title + '\n')


if __name__ == '__main__':
    HackerNewsSpider.start()
```

### How It Works?

`Spider` will read links in `start_urls`, and maintains a asynchronous queue.
The queue is a producer consumer model, and the loop will run until no more request functions.
