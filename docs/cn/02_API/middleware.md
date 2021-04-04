# Middleware
`Middleware`的主要作用是在进行一个请求的前后进行一些处理，比如监听请求或者响应：
- [Middleware().request](https://github.com/howie6879/ruia/blob/master/ruia/middleware.py)：在请求前处理一些事情
- [Middleware().response](https://github.com/howie6879/ruia/blob/master/ruia/middleware.py)：在请求后处理一些事情

## Usage
使用中间件有两点需要注意，一个是处理函数需要带上特定的参数，第二个是不需要返回值，具体使用如下：

```python
from ruia import Middleware

middleware = Middleware()

@middleware.request
async def print_on_request(spider_ins, request):
    """
    每次请求前都会调用此函数
    request: Request类的实例对象
    """
    print("request: print when a request is received")
    
@middleware.response
async def print_on_response(spider_ins, request, response):
    """
    每次请求后都会调用此函数
    request: Request类的实例对象
    response: Response类的实例对象
    """
    print("response: print when a response is received")
```

## How It Works?
`Middleware`通过装饰器来实现对函数的回调，从而让开发者可以优雅的实现中间件功能，`Middleware`类中的两个属性`request_middleware`和`response_middleware`分别维护着一个队列来处理开发者定义的处理函数