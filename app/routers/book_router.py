from fastapi import APIRouter, HTTPException, status

from app.collections.book_collection import BookCollection
from app.documents.book_document import BookDocument
from app.schemas.book_schema import (
    AddBookData,
    AddBookResponse,
    BookCreateModel,
    GetBooksResponse,
)

router = APIRouter(
    prefix="/books",
    tags=["Books"],
)


@router.post(
    "/",
    response_model=AddBookResponse,
    status_code=status.HTTP_201_CREATED,
    summary="책을 추가합니다",
)
async def add_book(book_data: BookCreateModel) -> AddBookResponse:
    # Create a BookDocument instance from the request data
    book_document = BookDocument(**book_data.model_dump())

    # Insert into the database
    inserted_id = await BookCollection.insert_book(document=book_document)
    return AddBookResponse(
        detail="책이 성공적으로 추가되었습니다.",
        added_book=AddBookData(inserted_id=inserted_id),
        status_code=status.HTTP_201_CREATED,
    )


@router.get(
    "/search/{book_title}",
    response_model=GetBooksResponse,
    status_code=status.HTTP_200_OK,
    summary="제목으로 책을 검색합니다. (유사한 제목 포함)",
)
async def get_books_by_title(book_title: str) -> GetBooksResponse:
    books = await BookCollection.select_book_by_book_title(book_title=book_title)
    if not books:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with title '{book_title}' not found",
        )
    return GetBooksResponse(
        detail="책을 성공적으로 찾았습니다.",
        books=books,
        status_code=status.HTTP_200_OK,
    )
