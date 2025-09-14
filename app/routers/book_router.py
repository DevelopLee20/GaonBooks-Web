from fastapi import APIRouter, HTTPException, status

from app.services.book_service import BookService
from app.schemas.book_schema import (
    AddBookData,
    AddBookResponse,
    BookCreateModel,
    DeleteBookResponse,
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
    inserted_id = await BookService.insert_book(book_data=book_data)

    if inserted_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="책 추가를 실패했습니다.",
        )

    return AddBookResponse(
        detail="책이 성공적으로 추가되었습니다.",
        added_book=AddBookData(inserted_id=inserted_id),
        status_code=status.HTTP_201_CREATED,
    )


@router.delete(
    "/{book_id}",
    response_model=DeleteBookResponse,
    status_code=status.HTTP_200_OK,
    summary="책을 삭제합니다.",
)
async def delete_book(book_id: str) -> DeleteBookResponse:
    if not await BookService.delete_book_by_id(book_id=book_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id '{book_id}' not found",
        )

    return DeleteBookResponse(
        detail="책이 성공적으로 삭제되었습니다.",
        status_code=status.HTTP_200_OK,
    )


@router.get(
    "/search/{book_title}",
    response_model=GetBooksResponse,
    status_code=status.HTTP_200_OK,
    summary="제목으로 책을 검색합니다. (유사한 제목 포함)",
)
async def get_books_by_title(book_title: str) -> GetBooksResponse:
    books = await BookService.select_books_by_title(book_title=book_title)

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
