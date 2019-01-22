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
    # Python 3.7 required
    asyncio.run(main())  

    # For python 3.6
    # loop = asyncio.new_event_loop()
    # loop.run_until_complete(main())

# Output:
# [2019:01:21 18:19:02]-Request-INFO  request: <GET: https://docs.python.org/3/>
# 3.7.2 Documentation
# tutorial/index.html

```

We hope you have already know python [asyncio](https://docs.python.org/3/library/asyncio.html) library,
and know its basic usage.
If not, remember the following tips:

* Functions defined with async keyword are now named coroutine;
* Define coroutine with async keyword;
* Call coroutine with await keyword;
* Start coroutine use `asyncio.run` function like the example.


Now focus on the screen output.
The first line is the log of `Ruia`,
and the following two lines are the data we want.

Okay, we have already finished the construction of our first Item.

## Data Cleaning

Now we get the version string: `3.7.2 Documentation`.
However, the `Documentation` is unnecessary.
Certainly we can solve this problem in such a way:

```python
import asyncio
from ruia import Item, TextField, AttrField


class PythonDocumentationItem(Item):
    title = TextField(css_select='title')
    tutorial_link = AttrField(xpath_select="//a[text()='Tutorial']", attr='href')


async def main():
    url = 'https://docs.python.org/3/'
    item = await PythonDocumentationItem.get_item(url=url)
    title = item.title.split(' ')[0]
    print(title)
    print(item.tutorial_link)


if __name__ == '__main__':
    # Python 3.7 required
    asyncio.run(main())  

    # For python 3.6
    # loop = asyncio.new_event_loop()
    # loop.run_until_complete(main())

# Output:
# [2019:01:21 18:19:02]-Request-INFO  request: <GET: https://docs.python.org/3/>
# 3.7.2
# tutorial/index.html

```

It works well, and it's okay if you like it.

Now consider such a way:

```python
import asyncio
from ruia import Item, TextField, AttrField


class PythonDocumentationItem(Item):
    title = TextField(css_select='title')
    tutorial_link = AttrField(xpath_select="//a[text()='Tutorial']", attr='href')
    
    def clean_title(self, value):
        return value.split(' ')[0]


async def main():
    url = 'https://docs.python.org/3/'
    item = await PythonDocumentationItem.get_item(url=url)
    print(item.title)
    print(item.tutorial_link)


if __name__ == '__main__':
    # Python 3.7 required
    asyncio.run(main())  

    # For python 3.6
    # loop = asyncio.new_event_loop()
    # loop.run_until_complete(main())

# Output:
# [2019:01:21 18:19:02]-Request-INFO  request: <GET: https://docs.python.org/3/>
# 3.7.2
# tutorial/index.html

```

Wow!
Now we directly get a pure version string from `item.title`.

`ruia` will automatically recognize methods starts with `clean_`.
If there's a field named `the_field`,
then its corresponding data cleaning method is `clean_the_field`.
Just add a prefix `clean_` is okay.

The default clean method of each field is just return the string itself.
Before data cleaning, fields are all pure python strings (sometimes a list or a dict of pure python strings).
If you want `item.index` to return a python integer,
please define `clean_index` method to `return int(value)`.

In `ruia`,
we tend to separate a crawler into two main parts:

* Data acquisition, for parsing HTML and create structured data;
* Data processing, for data persistence or some other operations.

Data acquisition is all in `Item` object,
including data cleaning.
And data processing will be introduced later,
in `ruia.Spider.parse` functions.
At data processing, we hope `item.field` return quite the value you want.
`ruia.Item` tries to avoid such operations:

```python
class MySpider(Spider):
    async def parse(self, response):
        item = MyItem.get_item(response)
        title = item.title.split(' ')[0]
        index = int(item.index)
        tags = [tag for tag in index.tags if tag not in ('not','wanted','tags')]
        print(title)
        print('The square of index: ', index ** 2)
        print('Tags: ', *tags)

```

We want to write such a clean code:

```python
class MySpider(Spider):
    async def parse(self, response):
        item = MyItem.get_item(response)
        print(item.title)
        print('The square of index: ', item.index ** 2)
        print('Tags: ', *item.tags)

```

It's more beautiful, isn't it?

## Get Many Items from One Page

Here's a HTML document.
It's simple and readable.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<div class="container">
    <div class="movie"><a class="title">Movie 1</a><span class="star">3</span></div>
    <div class="movie"><a class="title">Movie 2</a><span class="star">5</span></div>
    <div class="movie"><a class="title">Movie 3</a><span class="star">2</span></div>
    <div class="movie"><a class="title">Movie 4</a><span class="star">1</span></div>
    <div class="movie"><a class="title">Movie 5</a><span class="star">5</span></div>
</div>
</body>
</html>
```

It's a catalogue of movies.
We want to get the name of movies and their stars.

After analyzing document structure, we find that each movie is in a class `div.movie`.
Then we can navigate to the container element by a CSS Selector: `css_select='div.movie'`.
Then we can get our fields as before.

`ruia.Item` has a convenient way to finish this task.
If you define a `target_item` field to an Item,
then it stands for the container.
Here's an example.

```python
import asyncio
from ruia import Item, AttrField, TextField

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<div class="container">
    <div class="movie"><a class="title">Movie 1</a><span class="star">3</span></div>
    <div class="movie"><a class="title">Movie 2</a><span class="star">5</span></div>
    <div class="movie"><a class="title">Movie 3</a><span class="star">2</span></div>
    <div class="movie"><a class="title">Movie 4</a><span class="star">1</span></div>
    <div class="movie"><a class="title">Movie 5</a><span class="star">5</span></div>
</div>
</body>
</html>
"""


class MyItem(Item):
    target_item = TextField(css_select='.movie')
    title = TextField(css_select='.title')
    star = TextField(css_select='.star')

    def clean_star(self, value):
        return int(value)


async def main():
    items = await MyItem.get_items(html=HTML)
    for item in items:
        print(f'Title={item.title}, Star={item.star}')


if __name__ == '__main__':
    asyncio.run(main())  # Python 3.7 required

    # For python 3.6
    # loop = asyncio.new_event_loop()
    # loop.run_until_complete(main())

```

Previously, we call `Item.get_item(html=HTML)` to get an item.
Here, we call `Item.get_items(html=HTML)` to get a list of items.

The data cleaning methods still process a string, it has no difference.

```text
Output: 
Title=Movie 1, Star=3
Title=Movie 2, Star=5
Title=Movie 3, Star=2
Title=Movie 4, Star=1
Title=Movie 5, Star=5

```

## Get Many Value by One Field

Here is another example.
Consider that we are now at a movie detail page.
The HTML document shows like:


```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<div class="movie">
    <div class="title">Movie Title</div>
    <div class="star">5</div>
    <div class="tags">
        <div class="tag">Comedy</div>
        <div class="tag">2019</div>
        <div class="tag">China</div>
    </div>
</div>
</body>
</html>
```

We want to get the title, star, and tags of this movie.
Previously, we only pure strings from `Field`.
Here we want to get a list a pure strings from `tag` field.
`ruia.Item` provides an easy way, that is the `many=True` parameter of `Fields`.

Here is the implementation:

```python
import asyncio
from ruia import Item, TextField


HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<div class="movie">
    <div class="title">Movie Title</div>
    <div class="star">5</div>
    <div class="tags">
        <div class="tag">Comedy</div>
        <div class="tag">2019</div>
        <div class="tag">China</div>
    </div>
</div>
</body>
</html>
"""


class MyItem(Item):
    title = TextField(css_select='.title')
    star = TextField(css_select='.star')
    tags = TextField(css_select='.tag', many=True)

    def clean_star(self, value):
        return int(value)


async def main():
    item = await MyItem.get_item(html=HTML)
    print('Title: ', item.title)
    print('Star: ', item.star)
    for tag in item.tags:
        print('Tag: ', tag)


if __name__ == '__main__':
    asyncio.run(main())  # Python 3.7 required

    # For python 3.6
    # loop = asyncio.new_event_loop()
    # loop.run_until_complete(main())

```

As we can see, `tags` field return a list of tags.
All fields have this parameter.

## More Fields

Ruia supports more fields than `TextField` and `AttrField`.
However, they are the two fields that mostly used.

Ruia also supports `RegexField` for extract data from HTML document directly by regular expression.
It is only used for performance limitation, however, because of ruia's fast,
we seldom meet performance limitation.

There is a `HtmlField` to extract pure HTML source of a HTML element.

Read [Field API](../apis/field.md) to get more information.
