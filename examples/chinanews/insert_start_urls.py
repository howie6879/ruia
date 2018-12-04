import motor.motor_asyncio

db = motor.motor_asyncio.AsyncIOMotorClient('mongodb://admin:11QQqqWW@192.168.99.12')

async def ttt():
    x = await db.ruia_urlsdb.ChinaNews.insert_many([{"url":"http://www.chinanews.com/scroll-news/news1.html"}])
async def main():
    await ttt()

import asyncio
loop = asyncio.get_event_loop()
loop.run_until_complete(main())