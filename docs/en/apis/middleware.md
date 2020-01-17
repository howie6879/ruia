# Middleware

`Middleware` is mainly used to process before request and process after response,
such as listening request and response.

- [Middleware().request][middleware.py]: do some operations before request;
- [Middleware().response][middleware.py]: do some operations after response.

## Usage

Note:

* The function should receive a special argument;
* The function return nothing.

The arguments are listed in the following example:

```python
from ruia import Middleware

middleware = Middleware()

@middleware.request
async def print_on_request(spider_ins, request):
    """
    This function will be called before every request.
    request: an object of Request
    """
    print("request: print when a request is received")
    
@middleware.response
async def print_on_response(spider_ins, request, response):
    """
    This function will be called after every request.
    request: an object of Request
    response: an object of Response
    """
    print("response: print when a response is received")
```

## How It Works?

`Middleware` used decorators to implement the callback function, aims at writting middlewares easier for developers.

`Middleware().request_middleware` and `Middleware().response_middleware` are two queues, stands for the user-defined functions.

[middleware.py]: https://github.com/howie6879/ruia/blob/master/ruia/middleware.py
