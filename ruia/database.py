from motor.motor_asyncio import AsyncIOMotorClient
class UrlsDb:
    def __init__(self,url,database,collection):
        self.conn = AsyncIOMotorClient(url)
        self.database = self.conn[database]
        self.collection = collection

    async def get_start_urls(self):
        start_urls =  await self.database[self.collection].find().to_list(length=None)
        start_urls = [i['url'] for i in start_urls]
        return start_urls