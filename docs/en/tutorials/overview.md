# An Overview of Ruia

Ruia is An asynchronous web scraping micro-framework,
powered by `asyncio` and `aiohttp`, 
aims at making crawling url as convenient as possible.

Write less, run faster is its philosophy.

Ruia spider consists three **required** parts and two **optional** parts:

* Required:
    * [Fields](field.md), binding with text or attribute of a HTML element;
    * [Items](item.md), a collection of fields;
    * [Spider](spider.md), the entry point of ruia spider;   

* Optional:
    * [Middleware](middleware.md), used for processing request and response;
    * [Plugin](plugins.md), used for enhancing ruia functions.

Ruia also provides friendly [Request](request.md) and [Response](response.md) objects.

Follow the links to learn each part of this tutorial.
