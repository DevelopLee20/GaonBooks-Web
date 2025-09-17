from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from app.core.enums import STORE_SPOT
from app.core.security import get_current_user
from app.services.book_service import BookService
from app.schemas.book_schema import (
    AddBookData,
    AddBookResponse,
    BookCreateModel,
    DeleteBookResponse,
    GetBooksResponse,
    UploadBooksResponse,
)

router = APIRouter(
    prefix="/books",
    tags=["Books"],
)


@router.post(
    "/upload/excel",
    response_model=UploadBooksResponse,
    status_code=status.HTTP_201_CREATED,
    summary="엑셀 파일로 책 목록을 추가합니다.",
    dependencies=[Depends(get_current_user)],
)
async def upload_books_from_excel(
    store_spot: STORE_SPOT,
    file: UploadFile = File(...),
) -> UploadBooksResponse:
    (
        total_books_in_file,
        added_books_count,
        del_files,
    ) = await BookService.insert_all_books_to_file(store_spot=store_spot, file=file)

    return UploadBooksResponse(
        detail="엑셀 파일의 책 목록을 성공적으로 추가했습니다.",
        total_books_in_file=total_books_in_file,
        added_books_count=added_books_count,
        deleted_books_count=del_files,
        status_code=status.HTTP_201_CREATED,
    )


@router.post(
    "/",
    response_model=AddBookResponse,
    status_code=status.HTTP_201_CREATED,
    summary="책을 추가합니다",
    dependencies=[Depends(get_current_user)],
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
    dependencies=[Depends(get_current_user)],
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
async def get_books_by_title(
    book_title: str, store_spot: STORE_SPOT
) -> GetBooksResponse:
    books = await BookService.select_books_by_title(
        book_title=book_title, store_spot=store_spot
    )

    if not books:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"'{book_title}' 해당 제목의 도서를 찾을 수 없습니다.",
        )
    return GetBooksResponse(
        detail="책을 성공적으로 찾았습니다.",
        books=books,
        status_code=status.HTTP_200_OK,
    )
