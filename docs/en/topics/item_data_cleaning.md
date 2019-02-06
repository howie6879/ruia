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
    title = MyItem.get_item(response.html).title
    title = title.split(' | ')[0]
    with open('data.txt', mode='a') as file:
        file.writelines([title])
```

It works well.
However, in ruia, we want to separate the two processes:

* Data acquisition, for parsing HTML and create structured data;
* Data processing, for data persistence or some other operations.

We provide a better way for data cleaning.

```python
from ruia import Item, TextField

class MyItem(Item):
    title = TextField(css_select='title')
    
    def clean_title(self, value):
        value = value.split(' | ')[0]
        return value

async def parse(self, response):
    title = MyItem.get_item(response.html).title
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

Separate the two processes makes our code more readable.
