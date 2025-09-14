import io
import re
import pandas as pd
from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.core.enums import STORE_SPOT
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
)
async def upload_books_from_excel(
    store_spot: STORE_SPOT,
    file: UploadFile = File(...),
) -> UploadBooksResponse:
    if file.content_type not in [
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    ]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="엑셀 파일(.xlsx)만 업로드할 수 있습니다.",
        )

    contents = await file.read()
    df = pd.read_excel(io.BytesIO(contents), engine="openpyxl")

    df.columns = [
        "subject_name",
        "book_and_author",
        "publisher",
        "request_count",
        "received_count",
        "price",
        "fulfillment_rate",
        "major",
        "professor_name",
        "location",
        "order_count",
    ]

    added_books_count = 0
    total_books_in_file = len(df)

    for _, row in df.iterrows():
        book_title = row["book_and_author"]
        author = None

        match = re.search(r"\((.*?)\)", book_title)
        if match:
            author = match.group(1)
            book_title = book_title.replace(f"({author})", "").strip()

        book_data = BookCreateModel(
            store_spot=store_spot,
            subject_name=row.get("subject_name"),
            book_title=book_title,
            author=author,
            publisher=row.get("publisher"),
            request_count=row.get("request_count"),
            received_count=row.get("received_count"),
            price=row.get("price"),
            fulfillment_rate=row.get("fulfillment_rate"),
            major=row.get("major"),
            professor_name=row.get("professor_name"),
            location=row.get("location"),
            order_count=row.get("order_count"),
        )

        inserted_id = await BookService.insert_book(book_data=book_data)
        if inserted_id:
            added_books_count += 1

    return UploadBooksResponse(
        detail="엑셀 파일의 책 목록을 성공적으로 추가했습니다.",
        total_books_in_file=total_books_in_file,
        added_books_count=added_books_count,
        status_code=status.HTTP_201_CREATED,
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
