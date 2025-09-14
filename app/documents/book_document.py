import dataclasses
from pydantic import Field

from app.core.base_document import BaseModel
from app.core.enums import STORE_SPOT


@dataclasses.dataclass(kw_only=True, frozen=True)
class BookDocument(BaseModel):
    store_spot: STORE_SPOT = Field(..., description="지점명")
    subject_name: str | None = Field(..., description="과목명")
    book_title: str = Field(..., description="도서명")
    author: str | None = Field(..., description="저자")
    publisher: str | None = Field(..., description="출판사")
    request_count: int | None = Field(..., description="신청")
    received_count: int | None = Field(..., description="입고")
    price: int | None = Field(..., description="가격")
    fulfillment_rate: float | None = Field(..., description="입고율")
    major: str | None = Field(..., description="전공")
    professor_name: str | None = Field(..., description="교수명")
    location: str | None = Field(..., description="위치")
    order_count: int | None = Field(..., description="주문")
