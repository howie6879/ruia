# Request
`Request`的主要作用是方便地处理网络请求，最终返回一个[Response](./response.md)对象。

主要提供的方法有：
- [Request().fetch](https://github.com/howie6879/ruia/blob/master/ruia/request.py)：请求一个网页资源，可以单独使用
- [Request().fetch_callback](https://github.com/howie6879/ruia/blob/master/ruia/request.py)：为`Spider`类提供的和核心方法

## Core arguments
- url：请求的资源链接
- method：请求的方法，`GET`或者`POST`
- callback：回调函数
- headers：请求头
- load_js：目标网页是否需要加载js
- metadata：跨请求传递的一些数据
- request_config：请求配置
- request_session：`aiohttp`的请求session
- kwargs：请求目标资源可定义的其他参数

## Usage

通过上面的参数介绍可以知道，`Request`除了需要结合`Spider`使用，也可以单独使用：

```python
import asyncio

from ruia import Request

request = Request("https://news.ycombinator.com/")
response = asyncio.get_event_loop().run_until_complete(request.fetch())

# Output
# [2018-07-25 11:23:42,620]-Request-INFO  <GET: https://news.ycombinator.com/>
# <Response url[text]: https://news.ycombinator.com/ status:200 metadata:{}>
```

## How It Works?
`Request`通过对`aiohttp`和`pyppeteer`的封装来实现对网页资源的异步请求
