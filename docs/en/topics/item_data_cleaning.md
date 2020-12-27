# Item Data Cleaning

If you visit other's blog,
you may find that the titles of articles are often such a format: 
`Ruia is a great framework | Ruia's blog`.
Open the inspector of browser,
you will find such an element: 

```html
<title>Ruia is a great framework | Ruia's blog</title>
```

The title element contains two parts: the actual title of this article and the site name of the blog.

Now we just want to get the actual title `Ruia is a great framework`.
We can write a statement in `parse` method, like:

```python
from ruia import Item, TextField

class MyItem(Item):
    title = TextField(css_select='title')

async def parse(self, response):
    title = MyItem.get_item(await response.text()).title
    title = title.split(' | ')[0]
    with open('data.txt', mode='a') as file:
        file.writelines([title])
```

It works well.
However, in ruia, we want to separate the two processes:

* Data acquisition, for parsing HTML and create structured data;
* Data processing, for data persistence or some other operations.

By separating data acquisition and data processing,
our code can be more readable.
We provide a better way for data cleaning.

```python
from ruia import Item, TextField

class MyItem(Item):
    title = TextField(css_select='title')
    
    def clean_title(self, value):
        value = value.split(' | ')[0]
        return value

async def parse(self, response):
    title = MyItem.get_item(await response.text()).title
    with open('data.txt', mode='a') as file:
        file.writelines([title])
```

Now we get a better item.
We just get the property `title` of `item`, like `item.title`, 
and we can get a pure title we want.

`ruia` will automatically recognize methods starts with `clean_`.
If there's a field named `the_field`,
then its corresponding data cleaning method is `clean_the_field`.
Just add a prefix `clean_` is okay.

The default clean method of each field is just return the string itself.
Before data cleaning, fields are all pure python strings (sometimes a list or a dict of pure python strings).
If you want `item.index` to return a python integer,
please define `clean_index` method to `return int(value)`.

Now let's focus on such a HTML code.
For some reason, perhaps for css layout,
there are some empty items.
We want 5 movies, while ruia get 7.
Of course you can delete useless items in parse function,
however, it violated our principle that
we should separate get items and save items.

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
    <div class="movie"><a class="title"></a><span class="star"></span></div>
    <div class="movie"><a class="title"></a><span class="star"></span></div>
</div>
</body>
</html>
```

Ruia use an `Exception` to solve this problem.
In `clean_*` functions, we can raise a `ruia.IgnoreThisItem`
to skip useless items.
Here's a snippet as a demo.

```python
from ruia import Item, TextField, IgnoreThisItem

class MyItem(Item):
    target_item = TextField(css_select='.movie')
    title = TextField(css_select=".title")
    star = TextField(css_select=".star")

    @staticmethod
    async def clean_title(value):
        if not value:
            raise IgnoreThisItem
        return value


async def main():
    items = list()
    async for item in MyItem.get_items(html=HTML):
        items.append(item)
    assert len(items) == 5
```

Now, the length of items is 5, instead of 7.
