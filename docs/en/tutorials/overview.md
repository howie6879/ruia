# An Overview of Ruia

Ruia is An asynchronous web scraping micro-framework,
powered by `asyncio` and `aiohttp`, 
aims at making crawling url as convenient as possible.

**Write less, run faster** is Ruia's philosophy.

Ruia spider consists the following four parts:

* [Data Items](item.md), required, a collection of fields
* [Spider](spider.md), recommended, a manager to make your spider stronger
* [Middleware](middleware.md), optional, used for processing request and response
* [Plugin](plugins.md), optional, used to enhance ruia functions.

Ruia also provides friendly [Request & Response](request.md) objects,
follow the links to learn each part of this tutorial.
