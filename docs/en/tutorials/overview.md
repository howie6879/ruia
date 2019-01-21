# An Overview of Ruia

Ruia is An **asynchronous** web scraping micro-framework,
powered by `asyncio` and `aiohttp`, 
aims at making crawling url as convenient as possible.

**Write less, run faster** is Ruia's philosophy.

Ruia spider consists the following four parts:

|          Ruia Part             | Is Required  |                   Description              |
| ---------------------------    | ------------ | ------------------------------------------ |
| [Data Items](item.md)          | Required     | a collection of fields                     |
| [Spider](spider.md)            | Recommended  | a manager to make your spider stronger     |
| [Middleware](middleware.md)    | Optional     | used for processing request and response   |
| [Plugin](plugins.md)           | Optional     | used to enhance ruia functions             |
