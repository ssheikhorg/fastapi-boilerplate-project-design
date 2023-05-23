from typing import Any
from urllib.parse import quote_plus

from motor.motor_tornado import MotorClient
from pymongo import ReturnDocument
from pymongo.client_session import ClientSession
from pymongo.collection import Collection

from pymongo.mongo_client import MongoClient
from pymongo.results import InsertOneResult, InsertManyResult, UpdateResult, DeleteResult
from pymongo.server_api import ServerApi

from src import settings as c

_db_url = (
    f"mongodb://localhost:27017/"
)


class AsyncMongoDB:
    """A helper used to easily interact with a mongodb database."""

    def __init__(self, collection_name: str, db_name: str) -> None:
        if db_name == c.yl_db_name:
            self._collection = MotorClient(c.yl_db_url, server_api=ServerApi("1"))[db_name][collection_name]
        else:
            self._collection = MotorClient(_ym_db_url, server_api=ServerApi("1"))[db_name][collection_name]

    async def insert(self, **document: dict) -> InsertOneResult:
        """Insert one document"""
        result: InsertOneResult = await self._collection.insert_one(document)
        return result

    async def insert_many(self, **data: dict) -> InsertManyResult:
        """Insert many documents"""
        result: InsertManyResult = await self._collection.insert_many(data)
        return result

    async def get(self, query: dict) -> dict:
        """Find one document"""
        result: dict = await self._collection.find_one(query)
        if result:
            result["_id"] = result["_id"].__str__()
        return result

    async def get_many(self, query: dict, skip: int = 0, limit: int = 10, sort: tuple = None) -> list[dict]:
        """Find many documents"""
        if sort:
            result: list = (
                await self._collection.find(query)
                .sort(sort[0], sort[1])
                .skip(skip * limit)
                .limit(limit)
                .to_list(length=limit)
            )
        else:
            result = await self._collection.find(query, {"_id": 0}).skip(skip).limit(limit).to_list(length=limit)
        return [{k: v.__str__() if k == "_id" else v for k, v in i.items()} for i in result]

    async def count(self, query: dict) -> int:
        """Count documents"""
        result: int = await self._collection.count_documents(query)
        return result

    async def update(self, query: dict, data: dict, array_filters: list = None, upsert: bool = False) -> UpdateResult:
        """Update one document"""
        if array_filters:
            result: UpdateResult = await self._collection.update_one(
                query, data, array_filters=array_filters, upsert=upsert
            )
        else:
            result = await self._collection.update_one(query, data)
        return result

    async def update_many(self, query: dict, data: dict, upsert: bool = False) -> Any:
        """Update many documents"""
        return await self._collection.update_many(query, data, upsert=upsert)

    async def delete(self, query: dict) -> DeleteResult:
        """Delete one document"""
        result: DeleteResult = await self._collection.delete_one(query)
        return result

    async def aggregate(self, pipeline: list) -> list[dict]:
        """Aggregate documents"""
        result = await self._collection.aggregate(pipeline).to_list(length=None)
        return [{k: v.__str__() if k == "_id" else v for k, v in i.items()} for i in result]

    async def find_and_update(self, query: dict, data: dict) -> dict:
        """Find one and update document"""
        _update_kwargs = {"projection": {"_id": False}, "upsert": True, "return_document": ReturnDocument.AFTER}
        result: dict = await self._collection.find_one_and_update(query, data, **_update_kwargs)
        if result:
            result["_id"] = result["_id"].__str__()
        return result

    async def start_session(self) -> ClientSession:
        """Start session for transaction"""
        result: ClientSession = await self._collection.database.client.start_session()
        return result

    async def check_collection(self) -> bool:
        """Check if collection exists"""
        return self._collection.name in await self._collection.database.list_collection_names()

    async def create_collection(self) -> Collection:
        """Create collection"""
        result: Collection = await self._collection.database.create_collection(self._collection.name)
        return result

    async def create_index(self, index: list) -> str:
        """Create index"""
        result: str = await self._collection.create_index(index)
        return result

    async def index_exists(self, index: list) -> bool:
        """Check if index exists"""
        idx_list = await self._collection.index_information()
        for idx in idx_list:
            if idx_list[idx]["key"] == index:
                return True
        return False


class SyncMongoDB:
    """A helper used to easily interact with a mongodb database."""

    def __init__(self, collection_name: str, db_name: str) -> None:
        if db_name == c.yl_db_name:
            self._collection = MongoClient(c.yl_db_url, server_api=ServerApi("1"))[db_name][
                collection_name
            ]  # type: ignore
        else:
            self._collection = MongoClient(_ym_db_url, server_api=ServerApi("1"))[db_name][collection_name]

    def insert(self, data: dict) -> InsertOneResult:
        result: InsertOneResult = self._collection.insert_one(data)
        return result

    def get(self, query: dict) -> dict | None:
        result: dict | None = self._collection.find_one(query)
        if result:
            result["_id"] = result["_id"].__str__()
        return result


class MongoEvent:
    """A helper used to easily interact with a mongodb database."""

    def __init__(self) -> None:
        self.async_ym_client: MongoClient = MotorClient(_ym_db_url)
        self.async_yl_client: MongoClient = MotorClient(c.yl_db_url)
        self.sync_ym_client: MongoClient = MongoClient(_ym_db_url)
        self.sync_yl_client: MongoClient = MongoClient(c.yl_db_url)

    async def start(self) -> tuple:
        """on_event startup mongodb"""
        return self.async_ym_client, self.async_yl_client, self.sync_ym_client, self.sync_yl_client

    async def stop(self) -> None:
        """on_event shutdown mongodb"""
        self.async_ym_client.close()
        self.async_yl_client.close()
        self.sync_ym_client.close()
        self.sync_yl_client.close()


def db_collection(collection_name: str, db_name: str = c.ym_db_name) -> AsyncMongoDB:
    """Get mongodb database"""
    return AsyncMongoDB(collection_name, db_name)


def db_sync_collection(collection_name: str, db_name: str = c.ym_db_name) -> SyncMongoDB:
    """Get mongodb database"""
    return SyncMongoDB(collection_name, db_name)
