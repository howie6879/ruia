## Response

[Response](https://github.com/howie6879/aspider/blob/master/aspider/response.py)的目的是返回一个统一且友好的响应对象，主要属性如下：
- url：请求的资源链接
- metadata：跨请求传递的一些数据
- res_type：请求的资源类型，默认为`str`，可以选择`bytes`或`json`
- html：源网站返回的资源数据
- cookies：网站 cookies
- history：访问历史
- headers：请求头
- status：请求状态码