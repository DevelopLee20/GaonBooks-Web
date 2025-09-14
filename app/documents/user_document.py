import dataclasses
from pydantic import Field

from app.core.base_document import BaseModel
from app.core.enums import STORE_SPOT


@dataclasses.dataclass(kw_only=True, frozen=True)
class UserDocument(BaseModel):
    user_id: str = Field(..., description="사용자 아이디")
    hashed_password: str = Field(..., description="해시된 비밀번호")
    store_spot: STORE_SPOT = Field(..., description="지점명")
