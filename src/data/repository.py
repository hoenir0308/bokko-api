import motor.motor_asyncio
from pymongo import DESCENDING


class Repository:
    _instance = None

    def __new__(cls, url, database_name):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.client = motor.motor_asyncio.AsyncIOMotorClient(url)
            cls._instance.db = cls._instance.client[database_name]
        return cls._instance

    async def insert_one(self, collection_name: str, document: dict) -> str:
        collection = self.db[collection_name]
        result = await collection.insert_one(document)
        return result.inserted_id

    async def insert_many(self, collection_name: str, documents: list) -> list:
        collection = self.db[collection_name]
        result = await collection.insert_many(documents)
        return result.inserted_ids

    async def find_one(self, collection_name, query) -> dict:
        collection = self.db[collection_name]
        document = await collection.find_one(query)
        return document

    async def find_many(self, collection_name, query, sort_by=None, sort_direction=DESCENDING) -> list:
        collection = self.db[collection_name]
        documents = []
        cursor = collection.find(query)
        if sort_by:
            cursor = cursor.sort(sort_by, sort_direction)
        async for document in cursor:
            documents.append(document)
        return documents

    async def update_one(self, collection_name, query, update):
        collection = self.db[collection_name]
        result = await collection.update_one(query, {'$set': update})
        return result.modified_count

    async def delete_one(self, collection_name, query):
        collection = self.db[collection_name]
        result = await collection.delete_one(query)
        return result.deleted_count

    async def delete_many(self, collection_name, query):
        collection = self.db[collection_name]
        result = await collection.delete_many(query)
        return result.deleted_count

    async def get_count(self, collection_name, query):
        collection = self.db[collection_name]
        result = await collection.count_documents(query)
        return result