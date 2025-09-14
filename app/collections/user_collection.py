import dataclasses
from typing import Any

from app.core.database import db
from app.documents.user_document import UserDocument
from app.core.enums import STORE_SPOT


class UserCollection:
    _collection = db["user"]

    @classmethod
    def _parse(cls, document: dict[str, Any]) -> UserDocument:
        return UserDocument(
            _id=document["_id"],
            user_id=document["user_id"],
            hashed_password=document["hashed_password"],
            store_spot=STORE_SPOT(document["store_spot"]),
        )

    @classmethod
    async def get_user_by_user_id(cls, user_id: str) -> UserDocument | None:
        result = await cls._collection.find_one(filter={"user_id": user_id})
        if result:
            return cls._parse(result)
        return None

    @classmethod
    async def insert_user(cls, document: UserDocument) -> str | None:
        insert_data = dataclasses.asdict(document)
        insert_data.pop("_id", None)

        result = await cls._collection.insert_one(insert_data)

        if result.inserted_id:
            return str(result.inserted_id)

        return None
