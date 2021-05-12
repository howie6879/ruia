<p align="center"><img src="https://raw.githubusercontent.com/howie6879/ruia/master/docs/images/logo.png" width='120px' height='120px' alt="Ruia logo" >
</p>
<h1 align="center"><a href="https://github.com/howie6879/ruia" target="_blank">Ruia</a></h1>
<p align="center">🕸️ Async Python 3.6+ web scraping micro-framework based on asyncio.</p>
<p align="center"><strong>⚡ Write less, run faster.</strong></p>

<p align="center">
<a href="https://travis-ci.org/howie6879/ruia"><img src="https://travis-ci.org/howie6879/ruia.svg?branch=master" alt="travis"></a>
<a href="https://travis-ci.org/howie6879/ruia"><img src="https://codecov.io/gh/howie6879/ruia/branch/master/graph/badge.svg" alt="codecov"></a>
<a href="https://pypi.org/project/ruia"><img src="https://img.shields.io/pypi/pyversions/ruia.svg" alt="PyPI - Python Version"></a>
<a href="https://pypi.org/project/ruia/"><img src="https://img.shields.io/pypi/v/ruia.svg" alt="PyPI"></a>
<a href="https://pepy.tech/project/ruia"><img src="https://pepy.tech/badge/ruia/month" alt="Downloads"></a>
<a href="https://gitter.im/howie6879_ruia/communit"><img src="https://badges.gitter.im/Join%20Chat.svg" alt="gitter"></a>
</p>

![](https://raw.githubusercontent.com/howie6879/ruia/master/docs/images/ruia_demo.png)

## 概述

[**Ruia**](https://github.com/howie6879/ruia)是一个基于[asyncio](https://docs.python.org/3/library/asyncio.html)和[aiohttp](https://docs.aiohttp.org/en/stable/)的异步爬虫框架，目标在于让开发者编写爬虫尽可能地方便快速。

**写更少的代码，获取更快的运行速度**：

- 教程：[中文文档][doc_cn] |[documentation][doc_en]
- Github 组织： [python-ruia][Organization]
- 插件：[awesome-ruia][Awesome](你贡献的任何插件都是值得赞赏且可贵的！)

## 特性

- **简单**：简明的语法
- **速度**：
  - 开发：常用功能插件化，如[加载`js`][ruia-pyppeteer]、[自动切换`UA`][ruia-ua]、[数据持久化][ruia-motor]等插件
  - 运行：**asyncio**驱动
- **插件**：自由地扩展个性化功能

## 安装

``` shell
# For Linux & Mac
pip install -U ruia[uvloop]

# For Windows
pip install -U ruia

# New features
pip install git+https://github.com/howie6879/ruia
```

## 入门

1.  [Overview](https://docs.python-ruia.org/en/tutorials/overview.html)
2.  [Installation](https://docs.python-ruia.org/en/tutorials/installation.html)
3.  [Define Data Items](https://docs.python-ruia.org/en/tutorials/item.html)
4.  [Spider Control](https://docs.python-ruia.org/en/tutorials/spider.html)
5.  [Request & Response](https://docs.python-ruia.org/en/tutorials/request.html)
6.  [Customize Middleware](https://docs.python-ruia.org/en/tutorials/middleware.html)
7.  [Write a Plugins](https://docs.python-ruia.org/en/tutorials/plugins.html)

## 致谢

`Ruia`还处于开发阶段，任何`Issue`和`PR(Plugin)`都非常欢迎，感谢以下开发者对`Ruia`的贡献（排名不分先后）：

<!-- To get src for img: https://api.github.com/users/username -->
<a href="https://github.com/howie6879"><img src="https://avatars.githubusercontent.com/u/17047388?s=60&v=4" title="howie6879" width="50" height="50"></a>
<a href="https://github.com/panhaoyu"><img src="https://avatars.githubusercontent.com/u/23495987?s=60&v=4" title="panhaoyut" width="50" height="50"></a>
<a href="https://github.com/mirzazulfan"><img src="https://avatars.githubusercontent.com/u/36124339?s=64&v=4" title="mirzazulfan" width="50" height="50"></a>
<a href="https://github.com/abmyii"><img src="https://avatars.githubusercontent.com/u/52673001?s=60&v=4" title="abmyii" width="50" height="50"></a>
<a href="https://github.com/maxzheng"><img src="https://avatars.githubusercontent.com/u/9684260?s=60&v=4" title="maxzheng" width="50" height="50"></a>
<a href="https://github.com/ruter"><img src="https://avatars.githubusercontent.com/u/8568876?s=60&v=4" title="ruter" width="50" height="50"></a>
<a href="https://github.com/duolaAOA"><img src="https://avatars.githubusercontent.com/u/26339233?s=60&v=4" title="duolaAOA" width="50" height="50"></a>
<a href="https://github.com/fengdongfa1995"><img src="https://avatars.githubusercontent.com/u/20141092?s=60&v=4" title="fengdongfa1995" width="50" height="50"></a>
<a href="https://github.com/daijiangtian"><img src="https://avatars.githubusercontent.com/u/18069191?s=60&v=4" title="daijiangtian" width="50" height="50"></a>
<a href="https://github.com/scott-stoltzman-consulting"><img src="https://avatars.githubusercontent.com/u/66376167?s=60&v=4" title="consulting" width="50" height="50"></a>
<a href="https://github.com/Leezj9671"><img src="https://avatars.githubusercontent.com/u/11917826?s=60&v=4" title="Leezj9671" width="50" height="50"></a>

感谢以下框架：

- [aiohttp](https://github.com/aio-libs/aiohttp/)
- [demiurge](https://github.com/matiasb/demiurge)

## 交流

有任何问题，欢迎留言或者加我一起交流：

<div align=center><img width="300px" src="https://gitee.com/howie6879/oss/raw/master/uPic/qrcode_for_gh_3f02ace79dfb_258.jpg" /></div>

[doc_cn]: https://www.howie6879.cn/ruia/
[doc_en]: https://docs.python-ruia.org/
[Awesome]: https://github.com/python-ruia/awesome-ruia
[Organization]: https://github.com/python-ruia
[ruia-pyppeteer]: https://github.com/python-ruia/ruia-pyppeteer
[ruia-motor]: https://github.com/python-ruia/ruia-motor
[ruia-ua]: https://github.com/python-ruia/ruia-ua