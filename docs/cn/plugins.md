# Plugins

扩展的目的是将一些在爬虫程序中频繁使用的功能封装起来作为一个模块供第三方调用，**Ruia**通过`Middleware`来让开发者快速地实现第三方扩展

前面一节已经说过，`Middleware`的目的是对每次请求前后进行一番处理，然后我们实现了一个功能，就是在请求头里面加入`User-Agent`

可能任意一个爬虫都会需要自动添加随机`User-Agent`的功能，让我将这个功能封装下，使其成为**Ruia**的一个第三方扩展吧，让我们现在就开始吧

## Creating a project

项目名称为：[ruia-ua](https://github.com/ruia-plugins/ruia-ua)，因为**Ruia**基于`Python3.6+`，所以扩展`ruia-ua`也亦然，假设你此时使用的是`Python3.6+`，请按照如下操作：

```shell
# 安装包管理工具 pipenv
pip install pipenv
# 创建项目文件夹
mkdir ruia-ua
cd ruia-ua
# 安装虚拟环境
pipenv install 
# 安装 ruia
pipenv install ruia
# 安装 aiofiles
pipenv install aiofiles
# 创建项目目录
mkdir ruia_ua
cd ruia_ua 
# 实现代码放在这里
touch __init__.py	
```

目录结构如下：

```shell
ruia-ua
├── LICENSE					# 开源协议
├── Pipfile					# pipenv 管理工具生成文件
├── Pipfile.lock
├── README.md				
├── ruia_ua
│   ├── __init__.py			# 代码实现
│   └── user_agents.txt		# 随机ua集合
└── setup.py				
```

### First extension

`user_agents.txt`文件包含了各种`ua`，接下来我们只要利用**ruia**的`Middleware`实现在每次请求前随机添加一个`User-Agent`即可，实现代码如下：

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

编写完成后，我们只需要将`ruia-ua`上传至社区，这样所有的**ruia**使用者都可以直接使用你编写的第三方扩展，多么美好的一件事

### Usage

所有的爬虫程序都可以直接使用`ruia-ua`来实现自动添加`User-Agent`

```python
pip install ruia-ua
```

举个实际使用的例子：

```python
from ruia import AttrField, TextField, Item, Spider
from ruia_ua import middleware


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
    HackerNewsSpider.start(middleware=middleware)
```

第三方扩展的实现将会大大减少爬虫工程师的开发周期，**ruia**非常希望你可以开发并提交自己的第三方扩展