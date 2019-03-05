# Customize Middleware

`Middleware` is mainly used to process before request and process after response,
such as listening request and response.

Here is an example:

```python
from ruia import Spider, Middleware

middleware = Middleware()


@middleware.request
async def print_on_request(spider_ins, request):
    request.metadata = {
        'url': request.url
    }
    print(f"request: {request.metadata}")
    # Just operate request object, and do not return anything.


@middleware.response
async def print_on_response(spider_ins, request, response):
    print(f"response: {response.metadata}")


class MiddlewareSpiderDemo(Spider):
    start_urls = ['https://httpbin.org/get']
    concurrency = 10

    async def parse(self, response):
        pages = [f'https://httpbin.org/get?p={i}' for i in range(1, 2)]
        async for resp in self.multiple_request(urls=pages):
            print(resp.url)


if __name__ == '__main__':
    MiddlewareSpiderDemo.start(middleware=middleware)
```

If successful, your terminal will have the following output:

```python
[2019:03:05 15:20:03] INFO  Spider  Spider started!
[2019:03:05 15:20:03] INFO  Spider  Worker started: 4396957904
[2019:03:05 15:20:03] INFO  Spider  Worker started: 4396958040
[2019:03:05 15:20:03] INFO  Request <GET: https://httpbin.org/get>
request: {'url': 'https://httpbin.org/get'}
request: {'url': 'https://httpbin.org/get?p=1'}
[2019:03:05 15:20:05] INFO  Request <GET: https://httpbin.org/get?p=1>
[2019:03:05 15:20:06] INFO  Spider  Stopping spider: Ruia
[2019:03:05 15:20:06] INFO  Spider  Total requests: 2
[2019:03:05 15:20:06] INFO  Spider  Time usage: 0:00:02.531665
[2019:03:05 15:20:06] INFO  Spider  Spider finished!
response: {'url': 'https://httpbin.org/get?p=1'}
https://httpbin.org/get?p=1
response: {'url': 'https://httpbin.org/get'}
```

For full usage of Middleware, see [Middleware](../apis/middleware.md) API 

