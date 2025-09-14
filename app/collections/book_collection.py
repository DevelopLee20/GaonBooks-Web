import dataclasses
from typing import Any
from bson import ObjectId
from datetime import datetime
from typing import List

from app.core.database import db
from app.documents.book_document import BookDocument

class BookCollection:
    _collection = db["book"]

    @classmethod
    def _parse(cls, document: dict[str, Any]) -> BookDocument:
        return BookDocument(
            _id=document["_id"],
            store_spot=document["store_spot"],
            subject_name=document["subject_name"],
            book_title=document["book_title"],
            author=document["author"],
            publisher=document["publisher"],
            request_count=document["request_count"],
            received_count=document["received_count"],
            price=document["price"],
            fulfillment_rate=document["fulfillment_rate"],
            major=document["major"],
            professor_name=document["professor_name"],
            location=document["location"],
            order_count=document["order_count"],
            deleted_at=document.get("deleted_at"),
        )

    @classmethod
    async def insert_book(cls, document: BookDocument) -> str:
        insert_document = dataclasses.asdict(document)
        result = await cls._collection.insert_one(document=insert_document)

        return str(result.inserted_id)

    @classmethod
    async def soft_delete_book_by_id(cls, id: str) -> bool:
        result = await cls._collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": {"deleted_at": datetime.now()}},
        )
        return result.modified_count > 0

    @classmethod
    async def select_book_by_book_title(cls, book_title: str) -> List[BookDocument]:
        result = await cls._collection.find(
            filter={
                "book_title": {"$regex": book_title, "$options": "i"},
                "deleted_at": None,
            }
        ).to_list(length=None)

        return [cls._parse(document) for document in result]

    @classmethod
    async def select_all_book_by_store_spot(cls, store_spot: str) -> List[BookDocument]:
        result = await cls._collection.find(
            filter={
                "store_spot": store_spot,
                "deleted_at": None,
            }
        ).to_list(length=None)

        return [cls._parse(document) for document in result]
