import dataclasses
from typing import Annotated, Any

from bson import ObjectId
from pydantic import Field, BeforeValidator, PlainSerializer, WithJsonSchema


# Custom type for ObjectId to handle Pydantic v2 and JSON Schema
def validate_objectid(v: Any) -> ObjectId:
    if isinstance(v, ObjectId):
        return v
    if isinstance(v, str) and ObjectId.is_valid(v):
        return ObjectId(v)
    raise ValueError("Invalid ObjectId")

PydanticObjectId = Annotated[
    ObjectId,
    BeforeValidator(validate_objectid),
    PlainSerializer(lambda x: str(x), return_type=str),
    WithJsonSchema({"type": "string", "title": "ObjectId"}),
]


@dataclasses.dataclass(kw_only=True, frozen=True)
class BaseModel:
    _id: PydanticObjectId = dataclasses.field(default_factory=ObjectId)

    @property
    def id(self) -> PydanticObjectId | None:
        return self._id
