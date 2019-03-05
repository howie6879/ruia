# Request

`Request` is used for operating web requests.
It returns a [Response][response.md] object.

Methods: 

- [Request().fetch][request.py]: request a web resource, it can be used standalone
- [Request().fetch_callback][request.py]: it is a core method for `Spider` class

## Core arguments

- url: the resource link
- method: request method, shoud be `GET` or `POST
- callback: callback function
- encoding: html encode
- headers: request headers
- metadata: some data that need pass to next request
- request_config: the configure of the request
- request_session: `aiohttp.ClientSession`
- kwargs: other arguments for request

## Usage

From the arguments above, we can see that `Request` can be used both associated with `Spider` and standalone.

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

`Request` class will send asynchronous http request by packaging `aiohttp` and `pyppeteer`.

[response.md]: ./response.md
[request.py]: https://github.com/howie6879/ruia/blob/master/ruia/request.py
