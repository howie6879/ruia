# How to Write a Plugins

Plugins are used to package some common functions as a third-party model.
**Ruia** allow developers to implement third-party extensions in the following ways:

-   by using `Middleware` class 
-   by overwriting some core modules(just like Spider, Request etc...)

In the previous section, we talked about `Middleware`. 
It is used to process before request and after response.
Then, we implemeneted a function, that is to add `User-Agent` in request headers.

Perhaps any crawler need such a function, to add `User-Agent` randomly, so, let's packaging this function as a third-party extension.

Do it!

## Creating a project

The project name is [ruia-ua][ruia-ua]. 
**Ruia** is based on `Python3.6+`, so is `ruia-ua`.

Supposing that you're now in `Python 3.6+`.

```shell
# Install package management tool: pipenv
pip install pipenv
# Create project directory
mkdir ruia-ua
cd ruia-ua
# Install virtual environment
pipenv install 
# Install ruia
pipenv install ruia
# Install aiofiles
pipenv install aiofiles
# Create project directory in the project directory
mkdir ruia_ua
cd ruia_ua 
# Here's your implementation
touch __init__.py	
```

Directory structure:

```shell
ruia-ua
├── LICENSE					# Open source license
├── Pipfile					# pipenv management tools 
├── Pipfile.lock
├── README.md				
├── ruia_ua
│   ├── __init__.py			# Main code of your plugin
│   └── user_agents.txt		# some random user_agents
└── setup.py				
```

## First plugin

`user_agents.txt` contains all kinds of `UA`,
then we only need to use `Middleware` of `ruia` to add a random `User-Agent` before every request.

Here is one implementation:

```python
import os
import random

import aiofiles

from ruia import Middleware

__version__ = "0.0.1"


async def get_random_user_agent() -> str:
    """
    Get a random user agent string.
    :return: Random user agent string.
    """
    USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'
    return random.choice(await _get_data('./user_agents.txt', USER_AGENT))


async def _get_data(filename: str, default: str) -> list:
    """
    Get data from all user_agents
    :param filename: filename
    :param default: default value
    :return: data
    """
    root_folder = os.path.dirname(__file__)
    user_agents_file = os.path.join(root_folder, filename)
    try:
        async with aiofiles.open(user_agents_file, mode='r') as f:
            data = [_.strip() for _ in await f.readlines()]
    except:
        data = [default]
    return data


middleware = Middleware()


@middleware.request
async def add_random_ua(spider_ins, request):
    ua = await get_random_user_agent()
    if request.headers:
        request.headers.update({'User-Agent': ua})
    else:
        request.headers = {
            'User-Agent': ua
        }
```

Now it's high time to upload `ruia-ua` to community, then all other `ruia` users are able to use your third-party extension.
Sounds great!

## Usage

All crawlers can use `ruia-ua` to add `User-Agent` automatically.

```python
pip install ruia-ua
```

Here is an example:

```python
from ruia import AttrField, TextField, Item, Spider
from ruia_ua import middleware as ua_middleware


class HackerNewsItem(Item):
    target_item = TextField(css_select='tr.athing')
    title = TextField(css_select='a.storylink')
    url = AttrField(css_select='a.storylink', attr='href')

    async def clean_title(self, value):
        return value


class HackerNewsSpider(Spider):
    start_urls = ['https://news.ycombinator.com/news?p=1', 'https://news.ycombinator.com/news?p=2']
    concurrency = 10

    async def parse(self, response):
        async for item in HackerNewsItem.get_items(html=response.html):
            print(item.title)


if __name__ == '__main__':
    HackerNewsSpider.start(middleware=ua_middleware)
```

The implementations of third-party plugins will make developing crawlers easier!
**Ruia** do want your developing and uploading your own third-party plugins!

[ruia-ua]: https://github.com/ruia-plugins/ruia-ua
