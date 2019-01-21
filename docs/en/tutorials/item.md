# Define Data Item

## Item and Fields

First let's talk about what is `Item`.
`Item` is an important concept in `ruia`.
It defines what you want to get from HTML document.

`ruia.Item` is used to get data from HTML document and save structured data.

## Define Item

Here's an example of a simple Item.

```python
from ruia import Item, TextField, AttrField

class PythonDocumentationItem(Item):
    title = TextField(css_select='title')
    tutorial_link = AttrField(xpath_select="//a[text()='Tutorial']", attr='href')
```

Now let's reconstruct this Item.

## HTML document analyzing

Supposing that we want to get the current python documentation version
and its tutorial page link.

We read the HTML source at [https://docs.python.org/3/](https://docs.python.org/3/).

We find such two elements:

```html
<title>3.7.2 Documentation</title>
```

```html
<a class="biglink" href="tutorial/index.html">Tutorial</a>
```

What we want to do:
* navigate to the element;
* extract data from element.

## Navigate to an element

`Ruia` use selectors to navigate to the HTML element.
As a crawler engineer, 
`ruia` believes that you have a full knowledge of at least one of CSS Selector and XPath Selector.

For `title` element, because of his uniqueness, a simple CSS Selector is enough:

```python
css_select = 'title'
```

For the `Tuturial` element,
we have to use a XPath Selector to address it by it's text.

```python
xpath_select = "//a[text()='Tutorial']"
```

## Extract string from HTML element

Now we have navigated to HTML elements.
Time to extract string from it.
`Ruia` use `Field` to extract data from HTML elements.

For the `title` element, we want its `text` property.
`TextField` is quite suitable for this purpose.

```python
from ruia import TextField

title = TextField(css_select='title')

```

For the `Tutorial` element, we want its `href` property.
`AttrField` is useful now:

```python
from ruia import AttrField

tutorial_href = AttrField(xpath_select="//a[text()='Tutorial'", attr='href')

```

## Combine fields to a item

We have already told `ruia` how to find and extract data from HTML document.
It's high time to combine them together as a structured data.

```python
from ruia import Item, TextField, AttrField


class PythonDocumentationItem(Item):
    title = TextField(css_select='title')
    tutorial_link = AttrField(xpath_select="//a[text()='Tutorial']", attr='href')

```

We inherit a new Item named `HackerNewsItem` from `ruia.Item`.

Now, feed a HTML document to `PythonDocumentationItem`, it will extract the title and tutorial_link for us.

## Test this item

We just defined an item.
But will it perform just as what we want?
Let's have a simple test.

`Ruia.Item` has a convenient API.
It's normal that is it can extract data from HTML document as a string.
The magic is that it is also able to extract data from the given URL.

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

We hope you have already know python asyncio library,
and know its basic usage.
If not, remember the following tips:

* Functions with async keyword are now named coroutine;
* Define coroutine with async keyword;
* Call coroutine with await keyword;
* Start coroutine use `asyncio.run` function like the example.


Now focus on the screen output.
The first line is the log of `ruia`,
and the following two lines are the data we want.

Okay, we have already finished the construction of our first Item.

