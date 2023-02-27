from urllib.parse import quote_plus

from motor.motor_tornado import MotorClient
from pymongo import ReturnDocument

from src import settings as c

_db_url = (
    f"mongodb://localhost:27017/"
)


class MongoDB:
    """A helper used to easily interact with a mongodb database."""

    def __init__(self, collection_name: str, db_name: str = "test") -> None:
        self._collection = MotorClient(c.yl_db_url)[db_name][collection_name]

    async def insert_one_document(self, **data: Any) -> Any:
        """Insert one document"""
        return await self._collection.insert_one(data)

    async def insert_many_document(self, **data: Any) -> Any:
        """Insert many documents"""
        return await self._collection.insert_many(data)

    async def find_one_document(self, query: dict) -> Any:
        """Find one document"""
        return await self._collection.find_one(query, {"_id": 0})

    async def find_many_document(self, query: dict, skip: int = 0, limit: int = 10, sort: tuple = None) -> Any:
        """Find many documents"""
        if sort:
            return (
                await self._collection.find(query, {"_id": 0})
                .sort(sort[0], sort[1])
                .skip(skip)
                .limit(limit)
                .to_list(length=limit)
            )
        return await self._collection.find(query, {"_id": 0}).skip(skip).limit(limit).to_list(length=limit)

    async def count_document(self, query: dict) -> Any:
        """Count documents"""
        return await self._collection.count_documents(query)

    async def update_one_document(
        self, query: dict, data: dict, array_filters: Any = None, upsert: bool = False
    ) -> Any:
        """Update one document"""
        if array_filters:
            return await self._collection.update_one(query, data, array_filters=array_filters, upsert=upsert)
        return await self._collection.update_one(query, data)

    async def update_many_document(self, query: dict, data: dict, upsert: bool = False) -> Any:
        """Update many documents"""
        return await self._collection.update_many(query, data, upsert=upsert)

    async def find_one_and_update_document(self, query: dict, data: dict) -> Any:
        """Find one and update document"""
        _update_kwargs = {"projection": {"_id": False}, "upsert": True, "return_document": ReturnDocument.AFTER}
        return await self._collection.find_one_and_update(query, data, **_update_kwargs)

    async def start_session(self) -> Any:
        """Start session for transaction"""
        return await self._collection.database.client.start_session()

    async def aggregate_document(self, pipeline: list) -> Any:
        """Aggregate documents"""
        return await self._collection.aggregate(pipeline).to_list(length=None)

    async def delete_one_document(self, query: dict) -> Any:
        """Delete one document"""
        return await self._collection.delete_one(query)

    async def create_index(self, index: list) -> Any:
        """Create index"""
        return await self._collection.create_index(index)

    async def index_exists(self, index: list) -> bool:
        """Check if index exists"""
        idx_list = await self._collection.index_information()
        for idx in idx_list:
            if idx_list[idx]["key"] == index:
                return True
        return False


class MongoEvent:
    """A helper used to easily interact with a mongodb database."""

    def __init__(self) -> None:
        self.client_one = MotorClient("mongodb://localhost:27017/")
        self.client_two = MotorClient("mongodb://localhost:27017/")

    async def start(self) -> tuple:
        """on_event startup mongodb"""
        return self.ym_client, self.yl_client

    async def stop(self) -> None:
        """on_event shutdown mongodb"""
        self.ym_client.close()
        self.yl_client.close()


def db_collection(collection_name: str, db_name: str) -> MongoDB:
    """Get mongodb database"""
    return MongoDB(collection_name, db_name)
