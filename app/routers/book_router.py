import io
import re
import pandas as pd
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
    dependencies=[Depends(get_current_user)],
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

    del_files = await BookService.delete_books_by_store_spot(
        store_spot=store_spot.value
    )

    contents = await file.read()
    df = pd.read_excel(io.BytesIO(contents), engine="openpyxl")
    df = df.astype(object).where(pd.notna(df), None)

    if "도서명(저자)" not in df.columns:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="'도서명(저자)' 컬럼이 엑셀 파일에 존재하지 않습니다.",
        )

    added_books_count = 0
    total_books_in_file = len(df)

    for _, row in df.iterrows():
        book_title: str = row["도서명(저자)"]
        author = None

        if book_title is None:
            total_books_in_file -= 1
            continue

        match = re.search(r"\((.*?)\)", book_title)
        if match:
            author = match.group(1)
            book_title = book_title.replace(f"({author})", "").strip()

        book_data = BookCreateModel(
            store_spot=store_spot,
            subject_name=row.get("과목명"),
            book_title=book_title,
            author=author,
            publisher=row.get("출판사"),
            request_count=str(row.get("신청", "0")),
            received_count=str(row.get("입고", "0")),
            price=str(row.get("가격")),
            fulfillment_rate=str(row.get("입고율")),
            major=row.get("전공"),
            professor_name=row.get("교수명"),
            location=row.get("위치"),
            order_date=row.get("주문"),
        )

        inserted_id = await BookService.insert_book(book_data=book_data)
        if inserted_id:
            added_books_count += 1

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
