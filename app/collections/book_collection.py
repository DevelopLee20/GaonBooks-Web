import dataclasses
from typing import Any
from bson import ObjectId
from typing import List

from app.core.database import db
from app.documents.book_document import BookDocument
from app.core.enums import STORE_SPOT


class BookCollection:
    _collection = db["book"]

    @classmethod
    def _parse(cls, document: dict[str, Any]) -> BookDocument:
        return BookDocument(
            _id=document["_id"],
            store_spot=STORE_SPOT(document["store_spot"]),
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
            order_date=document["order_date"],
        )

    @classmethod
    async def insert_book(cls, document: BookDocument) -> str | None:
        insert_data = dataclasses.asdict(document)
        insert_data.pop("_id", None)

        result = await cls._collection.insert_one(insert_data)

        if result.inserted_id:
            return str(result.inserted_id)

        return None

    @classmethod
    async def delete_book_by_id(cls, id: str) -> bool:
        result = await cls._collection.delete_one(filter={"_id": ObjectId(id)})
        return result.deleted_count > 0

    @classmethod
    async def delete_books_by_store_spot(cls, store_spot: str) -> int:
        result = await cls._collection.delete_many(filter={"store_spot": store_spot})
        return result.deleted_count

    @classmethod
    async def select_book_by_book_title(cls, book_title: str, store_spot: STORE_SPOT) -> List[BookDocument]:
        result = await cls._collection.find(
            filter={
                "book_title": {"$regex": book_title, "$options": "i"},
                "store_spot": store_spot,
            }
        ).to_list(length=None)

        return [cls._parse(document) for document in result]

    @classmethod
    async def select_all_book_by_store_spot(cls, store_spot: str) -> List[BookDocument]:
        result = await cls._collection.find(
            filter={
                "store_spot": store_spot,
            }
        ).to_list(length=None)

        return [cls._parse(document) for document in result]
