from pydantic import BaseModel, Field
from typing import List

from app.core.base_response import BaseResponseModel
from app.core.enums import STORE_SPOT
from app.documents.book_document import BookDocument


class BookCreateModel(BaseModel):
    """Model for creating a new book, received from a client."""

    store_spot: STORE_SPOT = Field(..., description="지점명")
    subject_name: str | None = Field(..., description="과목명")
    book_title: str = Field(..., description="도서명")
    author: str | None = Field(..., description="저자")
    publisher: str | None = Field(..., description="출판사")
    request_count: int | None = Field(default=0, description="신청")
    received_count: int | None = Field(default=0, description="입고")
    price: int | None = Field(..., description="가격")
    fulfillment_rate: float | None = Field(default=0.0, description="입고율")
    major: str | None = Field(..., description="전공")
    professor_name: str | None = Field(..., description="교수명")
    location: str | None = Field(..., description="위치")
    order_count: int | None = Field(..., description="주문")


class AddBookData(BaseModel):
    inserted_id: str


class AddBookResponse(BaseResponseModel):
    added_book: AddBookData = Field(..., description="추가된 도서 정보")


class GetBooksResponse(BaseResponseModel):
    books: List[BookDocument] = Field(..., description="조회된 도서 목록")


class DeleteBookResponse(BaseResponseModel):
    pass


class UploadBooksResponse(BaseResponseModel):
    total_books_in_file: int = Field(..., description="엑셀 파일에 있는 총 책 수")
    added_books_count: int = Field(..., description="성공적으로 추가된 책 수")
