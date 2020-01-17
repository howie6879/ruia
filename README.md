<h1 align=center>
<img src="https://raw.githubusercontent.com/howie6879/ruia/master/docs/images/logo.png" width='120px' height='120px'>
</h1>

[![travis](https://travis-ci.org/howie6879/ruia.svg?branch=master)](https://travis-ci.org/howie6879/ruia) 
[![codecov](https://codecov.io/gh/howie6879/ruia/branch/master/graph/badge.svg)](https://codecov.io/gh/howie6879/ruia)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ruia.svg)](https://pypi.org/project/ruia/) 
[![PyPI](https://img.shields.io/pypi/v/ruia.svg)](https://pypi.org/project/ruia/) 
[![Downloads](https://pepy.tech/badge/ruia/month)](https://pepy.tech/project/ruia/month)
[![gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/howie6879_ruia/community)

![](https://raw.githubusercontent.com/howie6879/ruia/master/docs/images/ruia_demo.png)

## Overview

Ruia is an async web scraping micro-framework, written with `asyncio` and `aiohttp`, 
aims to make crawling url as convenient as possible.

**Write less, run faster**:

-   Documentation: [中文文档][doc_cn] |[documentation][doc_en]
-   Organization: [python-ruia][Organization]

## Features

-   **Easy**: Declarative programming
-   **Fast**: Powered by asyncio
-   **Extensible**: Middlewares and plugins
-   **Powerful**: JavaScript support

## Installation

``` shell
# For Linux & Mac
pip install -U ruia[uvloop]

# For Windows
pip install -U ruia

# New features
pip install git+https://github.com/howie6879/ruia
```

## Tutorials

1.  [Overview](https://docs.python-ruia.org/en/tutorials/overview.html)
2.  [Installation](https://docs.python-ruia.org/en/tutorials/installation.html)
3.  [Define Data Items](https://docs.python-ruia.org/en/tutorials/item.html)
4.  [Spider Control](https://docs.python-ruia.org/en/tutorials/spider.html)
5.  [Request & Response](https://docs.python-ruia.org/en/tutorials/request.html)
6.  [Customize Middleware](https://docs.python-ruia.org/en/tutorials/middleware.html)
7.  [Write a Plugins](https://docs.python-ruia.org/en/tutorials/plugins.html)


## TODO

-   Cache for debug, to decreasing request limitation
-   Distributed crawling/scraping

## Contribution

Ruia is still under developing, feel free to open issues and pull requests:

-   Report or fix bugs
-   Require or publish plugins
-   Write or fix documentation
-   Add test cases

!!!Notice: We use [black](https://github.com/psf/black) to format the code

## Thanks

-   [aiohttp](https://github.com/aio-libs/aiohttp/)
-   [demiurge](https://github.com/matiasb/demiurge)

[doc_cn]: https://github.com/howie6879/ruia/blob/master/docs/cn/README.md
[doc_en]: https://docs.python-ruia.org/
[Awesome]: https://github.com/python-ruia/awesome-ruia
[Organization]: https://github.com/python-ruia
