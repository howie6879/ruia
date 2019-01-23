# Request & Response

`Ruia` provides friendly and convenient `Request` and `Response` APis.

Here is an example:

```python
import asyncio
from ruia import Request


async def request_example():
    url = 'http://www.httpbin.org/get'
    params = {
        'name': 'ruia',
    }
    headers = {
        'User-Agent': 'Python3.6',
    }
    request = Request(url=url, method='GET', res_type='json', params=params, headers=headers)
    response = await request.fetch()
    assert response.html['args']['name'] == 'ruia'
    assert response.html['headers']['User-Agent'] == 'Python3.6'


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(request_example())

```

We define a request by class `Request`.
Then, we call `await request.fetch()` to get it's response.

!!!note
    `ruia.Request` provides asynchronous methods,
    be sure to use it in an asynchronous function with `async` statement,
    and get it's respones with `await` statement.


For full usage of response and request, see [Request API](../apis/request.md) and [Response API](../apis/response.md)