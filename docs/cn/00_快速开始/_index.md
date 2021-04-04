---
weight: 1
bookFlatSection: false
title: "快速开始"
---

# 快速开始

> 基于[Ruia](https://github.com/howie6879/ruia/)快速实现一个以[Hacker News](https://news.ycombinator.com/news)为目标的爬虫

本文主要通过对[Hacker News](https://news.ycombinator.com/news)的爬取示例来展示如何使用[**Ruia**](https://github.com/howie6879/ruia/)，下图红框中的数据就是爬虫脚本需要爬取的目标：

![5tjtPq](https://gitee.com/howie6879/oss/raw/master/uPic/5tjtPq.jpg)

开始前的准备工作：

- [x] 确定已经安装[**Ruia**](https://github.com/howie6879/ruia/)：`pip install ruia -U`
- [x] 确定可以访问[Hacker News](https://news.ycombinator.com/news)

## 第一步：定义 Item

`Item`的目的是定义目标网站中你需要爬取的数据，此时，爬虫的目标数据就是页面中的`Title`和`Url`，怎么提取数据，[**Ruia**](https://github.com/howie6879/ruia/)的[Field](https://github.com/howie6879/ruia/blob/master/ruia/field.py)类提供了以下三种方式提取目标数据：

- [XPath](https://www.w3schools.com/xml/xpath_intro.asp)
- [Re](https://www.w3schools.com/python/python_regex.asp)
- [CSS Selector](https://www.w3schools.com/cssref/css_selectors.asp)

这里我们使用`CSS Selector`来提取目标数据，用浏览器打开[Hacker News](https://news.ycombinator.com/news)，右键审查元素：

![ykAo8i](https://gitee.com/howie6879/oss/raw/master/uPic/ykAo8i.jpg)

> Notice: 本教程爬虫例子都默认使用CSS Selector的规则来提取目标数据

显而易见，每页包含`30`条资讯，那么目标数据的规则可以总结为：

| Param       | Rule              | Description              |
| :---------- | ----------------- | ------------------------ |
| target_item | tr.athing         | 表示每条资讯             |
| title       | a.storylink       | 表示每条资讯里的标题     |
| url         | a.storylink->href | 表示每条资讯里标题的链接 |

规则明确之后，就可以用`Item`来实现一个针对于目标数据的ORM，创建文件`items.py`，复制下面代码：

```python
from ruia import AttrField, TextField, Item


class HackerNewsItem(Item):
    target_item = TextField(css_select='tr.athing')
    title = TextField(css_select='a.storylink')
    url = AttrField(css_select='a.storylink', attr='href')
```

这段代码含义是：针对我们提取的目标`HTML`，我们定义了一个`HackerNewsItem`类，其包含了两个`field`：

- `title`：直接从文本提取
- `url`：从属性提取

等等！`target_item`是什么？对于一个`Item`类来说，当其定义好网页目标数据后，`Ruia`提供两种方式进行获取`Item`：

- get_item：获取网页的单目标，比如目标网页的标题，此时无需定义`target_item`；
- get_items：获取网页的多目标，比如当前目标网页[Hacker News](https://news.ycombinator.com/news)中的`title`和`url`一共有`30`个，这时就必须定义`target_item`来寻找多个目标块；`target_item`的作用就是针对这样的工作而诞生的，开发者只要定义好这个属性（此时Ruia会自动获取网页中`30`个`target_item`），然后每个`target_item`里面包含的`title`和`url`就会被提取出来。

## 第二步：测试 Item

[**Ruia**](https://github.com/howie6879/ruia/)为了方便扩展以及自由地组合使用，本身各个模块之间耦合度是极低的，每个模块都可以在你的项目中单独使用；你甚至只使用`ruia.Item`、`Ruia.TextField`和`ruia.AttrField`来编写一个简单的爬虫。

### 脚本调试

基于这个特性，我们可以直接在脚本里面测试`HackerNewsItem`：

```python
import asyncio

from ruia import Item, TextField, AttrField


class HackerNewsItem(Item):
    target_item = TextField(css_select='tr.athing')
    title = TextField(css_select='a.storylink')
    url = AttrField(css_select='a.storylink', attr='href')


async def test_item():
    url = 'https://news.ycombinator.com/news?p=1'
    async for item in HackerNewsItem.get_items(url=url):
        print('{}: {}'.format(item.title, item.url))


if __name__ == '__main__':
    # Python 3.7 Required.
    asyncio.run(test_item()) 

    # For Python 3.6
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(test_item())
```

接下来，终端会输出以下日志：

```shell
[2021:04:04 21:37:23] INFO  Request <GET: https://news.ycombinator.com/news?p=1>
How to bypass Cloudflare bot protection: https://jychp.medium.com/how-to-bypass-cloudflare-bot-protection-1f2c6c0c36fb
The EU has archived all of the “Euromyths” printed in UK media: https://www.thelondoneconomic.com/news/the-eu-have-archived-all-of-the-euromyths-printed-in-uk-media-and-it-makes-for-some-disturbing-reading-108942/
Laser: Learning a Latent Action Space for Efficient Reinforcement Learning: https://arxiv.org/abs/2103.15793
StyleCLIP: Text-Driven Manipulation of StyleGAN Imagery: https://github.com/orpatashnik/StyleCLIP
```

### 终端调试

为了使[**Ruia**](https://github.com/howie6879/ruia/)的脚本调试过程更加方便优雅，开发者还可以直接使用[ruia-shell](https://github.com/python-ruia/ruia-shell)插件进行调试，首先进行安装：

```shell
pip install -U ruia-shell
pip install ipython
```

具体使用如下：

```shell
➜  ~  ruia_shell https://news.ycombinator.com/news\?p\=1
            ✨ Write less, run faster(0.8.2).
__________      .__                .__           .__  .__
\______   \__ __|__|____      _____|  |__   ____ |  | |  |
 |       _/  |  \  \__  \    /  ___/  |  \_/ __ \|  | |  |
 |    |   \  |  /  |/ __ \_  \___ \|   Y  \  ___/|  |_|  |__
 |____|_  /____/|__(____  / /____  >___|  /\___  >____/____/
        \/              \/       \/     \/     \/
Available Objects   :
    response            :   ruia.Response
    request             :   ruia.Request
Available Functions :
    attr_field          :   Extract attribute elements by using css selector or xpath
    text_field          :   Extract text elements by using css selector or xpath
    fetch               :   Fetch a URL or ruia.Request
In [1]: request
Out[1]: <GET https://news.ycombinator.com/news?p=1>
In [2]: response
Out[2]: <Response url[GET]: https://news.ycombinator.com/news?p=1 status:200>
In [3]: text_field(css_select="a.storylink")
Out[3]: 'The EU has archived all of the “Euromyths” printed in UK media'
In [4]: attr_field(css_select="a.storylink", attr="href")
Out[4]: 'https://www.thelondoneconomic.com/news/the-eu-have-archived-all-of-the-euromyths-printed-in-uk-media-and-it-makes-for-some-disturbing-reading-108942/'
```

如果文字不清楚，可看下图：

![hHjQsh](https://gitee.com/howie6879/oss/raw/master/uPic/hHjQsh.png)

### 第三步：编写 Spider

`Ruia.Spider`是`Ruia`框架里面的核心控制类，它作用在于：

- 控制目标网页的请求`Ruia.Request`和响应`Ruia.Response`
- 可加载自定义钩子、插件、以及相关配置等，让开发效率更高

接下来会基于前面的`Item`脚本继续开发，具体代码如下：

```python
"""
 Target: https://news.ycombinator.com/
 pip install aiofiles
"""
import aiofiles

from ruia import Item, TextField, AttrField, Spider


class HackerNewsItem(Item):
    target_item = TextField(css_select='tr.athing')
    title = TextField(css_select='a.storylink')
    url = AttrField(css_select='a.storylink', attr='href')


class HackerNewsSpider(Spider):
    
    start_urls = [f'https://news.ycombinator.com/news?p={index}' for index in range(3)]
    concurrency = 3
    # 设置代理
    # aiohttp_kwargs = {"proxy": "http://0.0.0.0:8765"}

    async def parse(self, response):
        async for item in HackerNewsItem.get_items(html=await response.text()):
            yield item

    async def process_item(self, item: HackerNewsItem):
        """Ruia build-in method"""
        async with aiofiles.open('./hacker_news.txt', 'a') as f:
            await f.write(str(item.title) + '\n')
```

本段代码的作用是：

> 爬取[Hacker News](https://news.ycombinator.com/news)的前三页内容，设置并发数为`3`，然后全部持久化到文件`hacker_news.txt`

开发者实现`HackerNewsSpider`必须是`Spider`的子类，代码中出现的两个方法都是`Spider`内置的：

- parse：此方法是`Spider`的入口，每一个`start_urls`的响应必然会被`parse`方法捕捉并执行；
- process_item：此方法作用是抽离出对`Item`提取结果的处理过程，比如这里会接受自定义`Item`类作为输入，然后进行处理持久化到文件。

## 第四步：Start

>  希望[Ruia](https://github.com/howie6879/ruia/)可以为你带来编写爬虫的乐趣 ：)

一切准备就绪，启动你的爬虫脚本吧！

```python
import aiofiles

from ruia import AttrField, Item, Spider, TextField


class HackerNewsItem(Item):
    target_item = TextField(css_select="tr.athing")
    title = TextField(css_select="a.storylink")
    url = AttrField(css_select="a.storylink", attr="href")


class HackerNewsSpider(Spider):

    start_urls = [f"https://news.ycombinator.com/news?p={index}" for index in range(3)]
    concurrency = 3

    async def parse(self, response):
        async for item in HackerNewsItem.get_items(html=await response.text()):
            yield item

    async def process_item(self, item: HackerNewsItem):
        """Ruia build-in method"""
        async with aiofiles.open("./hacker_news.txt", "a") as f:
            await f.write(str(item.title) + "\n")


if __name__ == "__main__":
    HackerNewsSpider.start()
```

> Tips：如果你想在异步函数里面调用，执行`await HackerNewsSpider.start() `即可

不到`30`行代码，你就实现了对[Hacker News](https://news.ycombinator.com/news)的爬虫脚本，并且脚本带有自动重试、并发控制、语法简单等特性。

通过这个例子，你已经基本掌握了[Ruia](https://github.com/howie6879/ruia/)中`Item`、`Middleware`、`Request`等模块的用法，结合自身需求，你可以编写任何爬虫，例子代码见[hacker_news_spider](https://github.com/howie6879/ruia/blob/master/examples/topics_examples/hacker_news_spider.py)。

## 第五步：扩展

### Middleware

`Middleware`的目的是对每次请求前后进行一番处理，分下面两种情况：

- 在每次请求之前做一些事
- 在每次请求后做一些事

比如此时爬取[Hacker News](https://news.ycombinator.com/news)，若希望在每次请求时候自动添加`Headers`的`User-Agent`，可以添加以下代码引入中间件：

```python
from ruia import AttrField, Item, Middleware, Spider, TextField

middleware = Middleware()


@middleware.request
async def print_on_request(spider_ins, request):
    ua = "ruia user-agent"
    request.headers.update({"User-Agent": ua})
    print(request.headers)


class HackerNewsItem(Item):
    target_item = TextField(css_select="tr.athing")
    title = TextField(css_select="a.storylink")
    url = AttrField(css_select="a.storylink", attr="href")


class HackerNewsSpider(Spider):

    start_urls = [f"https://news.ycombinator.com/news?p={index}" for index in range(3)]
    concurrency = 3

    async def parse(self, response):
        async for item in HackerNewsItem.get_items(html=await response.text()):
            yield item


if __name__ == "__main__":
    HackerNewsSpider.start(middleware=middleware)
```

这样，程序会在爬虫请求网页资源之前自动加上`User-Agent`，针对自动`UA`的功能点，[Ruia](https://github.com/howie6879/ruia/)已经专门编写了一个名为[ruia-ua](https://github.com/python-ruia/ruia-ua)的插件来为开发者提升效率，使用非常简单，代码示例如下：

```python
from ruia import AttrField, TextField, Item, Spider
from ruia_ua import middleware


class HackerNewsItem(Item):
    target_item = TextField(css_select='tr.athing')
    title = TextField(css_select='a.storylink')
    url = AttrField(css_select='a.storylink', attr='href')


class HackerNewsSpider(Spider):
    start_urls = ['https://news.ycombinator.com/news?p=1', 'https://news.ycombinator.com/news?p=2']

    async def parse(self, response):
        # Do something...
        print(response.url)


if __name__ == '__main__':
    HackerNewsSpider.start(middleware=middleware)
```

### MongoDB

对于数据持久化，你可以按照自己喜欢的方式去做，前面实例中介绍了如何将目标`Item`持久化到文件中。

如果想将数据持久化到数据库（MongoDB）中，该怎么做？此时就到了凸显[Ruia](https://github.com/howie6879/ruia/)插件优势的时候了，你只需要安装[ruia-motor](https://github.com/python-ruia/ruia-motor)：

```shell
pip install -U ruia-motor
```

然后再代码中引入`ruia-motor`：

```python
from ruia_motor import RuiaMotorInsert, init_spider

from ruia import AttrField, Item, Spider, TextField


class HackerNewsItem(Item):
    target_item = TextField(css_select="tr.athing")
    title = TextField(css_select="a.storylink")
    url = AttrField(css_select="a.storylink", attr="href")


class HackerNewsSpider(Spider):
    start_urls = [f"https://news.ycombinator.com/news?p={index}" for index in range(3)]
    concurrency = 3
    # aiohttp_kwargs = {"proxy": "http://0.0.0.0:1087"}

    async def parse(self, response):
        async for item in HackerNewsItem.get_items(html=await response.text()):
            yield RuiaMotorInsert(collection="news", data=item.results)


async def init_plugins_after_start(spider_ins):
    spider_ins.mongodb_config = {"host": "127.0.0.1", "port": 27017, "db": "ruia_motor"}
    init_spider(spider_ins=spider_ins)


if __name__ == "__main__":
    HackerNewsSpider.start(after_start=init_plugins_after_start)
```

数据库中可以看到目标字段：

![ipuxKH](https://gitee.com/howie6879/oss/raw/master/uPic/ipuxKH.jpg)

是不是更简单了呢？