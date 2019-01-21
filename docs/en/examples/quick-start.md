# Quick Start

This essay will create a basic crawler with only
`ruia.Item`, `ruia.AttrField` and `ruia.TextField`.

## Item and Fields

First let's talk about `Item`.
`Item` is an important concept in `ruia`.
It defines what you want to get from HTML document.

Let's draw an analogue between `ruia.Item` and python standard `dict` class.
`Item` is like a container, it is like a `dict`, and contains many fields.
`Field` is like a `dict` key, 
and strings extracted from HTML document is saved 
like the `dict` value of corresponding key.

## Define Item

Here's an example of defining an `Item`.
Supposing that we want to get the current python documentation version
and its tutorial page link.

We read the HTML source at [https://docs.python.org/3/](https://docs.python.org/3/).
We find such two elements: 
`<title>3.7.2 Documentation</title>`,
`<a class="biglink" href="tutorial/index.html">Tutorial</a>`.

We can select element `title` by CSS Selector: `css_select='title'`
and select anchor element by XPath Selector: `xpath_select="//a[text()='Tutorial']"`
As a crawler engineer, `ruia` assumes you to know at least one of CSS Selector and XPath Selector.

Now we can define our `PythonDocumentationItem`:

```python
import asyncio
from ruia import Item, TextField, AttrField


class PythonDocumentationItem(Item):
    title = TextField(css_select='title')
    tutorial_link = AttrField(xpath_select="//a[text()='Tutorial']", attr='href')

```

We inherit a new Item named `HackerNewsItem` from `ruia.Item`.

## Run Crawler

`Item` class provides a friendly API to extract data directly by URL.

```python
import asyncio
from ruia import Item, TextField, AttrField


class PythonDocumentationItem(Item):
    title = TextField(css_select='title')
    tutorial_link = AttrField(xpath_select="//a[text()='Tutorial']", attr='href')


async def main():
    url = 'https://docs.python.org/3/'
    item = await PythonDocumentationItem.get_item(url=url)
    print(item.title)
    print(item.tutorial_link)


if __name__ == '__main__':
    asyncio.run(main())  # Python 3.7 required

    # For python 3.6
    # loop = asyncio.new_event_loop()
    # loop.run_until_complete(main())

# Output:
# [2019:01:21 18:19:02]-Request-INFO  request: <GET: https://docs.python.org/3/>
# 3.7.2 Documentation
# tutorial/index.html

```

The first line is the log of `ruia`,
and the following two lines are the data we want.

Okay, we have already finished our first crawler powered by `ruia`.
It did nothing, but tells us the basic conception of `ruia`.

Here is a more [useful example](typical.md), crawling data from Hacker News.

