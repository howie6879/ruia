# Response

[Response][response.py] is used to return a uniformed and friendly response object.

Main properties:

- url: the href of resource
- method: request method, shoud be `GET` or `POST
- encoding: html encode
- html: HTML source code from website
- metadata: some data that need pass to next request
- cookies: cookies of website
- history: the request history
- headers: response headers
- status: response status code
- aws_json: get json data from target url
- aws_read: get bytes data from target url
- aws_text: get text data from target url

[response.py]: https://github.com/howie6879/ruia/blob/master/ruia/response.py
