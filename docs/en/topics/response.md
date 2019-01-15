## Response

[Response][response.py] is used to return a uniformed and friendly response object.

Main properties:

- url: the href of resource
- metadata: some data from previous request
- res_type: the type of response, default `str`, optional `bytes` or `json`
- html: HTML source code from website
- cookies: cookies of website
- history: the request history
- headers: response headers
- status: response status code

[response.py]: https://github.com/howie6879/ruia/blob/master/ruia/response.py
