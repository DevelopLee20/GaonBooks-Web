from typing import List
from fastapi import UploadFile, HTTPException, status
import os
from datetime import datetime
import io
import pandas as pd

from app.core.enums import STORE_SPOT
from app.schemas.book_schema import BookCreateModel
from app.documents.book_document import BookDocument
from app.collections.book_collection import BookCollection


class BookService:
    @classmethod
    async def insert_book(cls, book_data: BookCreateModel) -> str | None:
        book_document = BookDocument(
            store_spot=book_data.store_spot,
            subject_name=book_data.subject_name,
            book_title=book_data.book_title,
            author=book_data.author,
            publisher=book_data.publisher,
            request_count=book_data.request_count,
            received_count=book_data.received_count,
            price=book_data.price,
            fulfillment_rate=book_data.fulfillment_rate,
            major=book_data.major,
            professor_name=book_data.professor_name,
            location=book_data.location,
            order_date=book_data.order_date,
        )
        inserted_id = await BookCollection.insert_book(document=book_document)

        return inserted_id

    @classmethod
    async def delete_book_by_id(cls, book_id: str) -> bool:
        return await BookCollection.delete_book_by_id(id=book_id)

    @classmethod
    async def delete_books_by_store_spot(cls, store_spot: str) -> int:
        return await BookCollection.delete_books_by_store_spot(store_spot=store_spot)

    @classmethod
    async def select_books_by_title(
        cls, book_title: str, store_spot: STORE_SPOT
    ) -> List[BookDocument]:
        books = await BookCollection.select_book_by_book_title(
            book_title=book_title, store_spot=store_spot
        )

        return books

    @classmethod
    async def insert_all_books_to_file(
        cls, store_spot: STORE_SPOT, file: UploadFile
    ) -> tuple[int, int, int]:
        ext = os.path.splitext(file.filename)[1].lower()

        if ext not in [".xls", ".xlsx", ".xlsm", ".xltm"]:
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

            order_date = row.get("주문")
            try:
                # order_date를 datetime으로 변환
                if isinstance(order_date, str):
                    order_date = datetime.strptime(order_date, "%Y-%m-%d")
            except ValueError:
                order_date = None

            book_data = BookCreateModel(
                store_spot=store_spot,
                subject_name=str(row.get("과목명")),
                book_title=str(book_title),
                author=str(author),
                publisher=str(row.get("출판사")),
                request_count=str(row.get("신청", "0")),
                received_count=str(row.get("입고", "0")),
                price=str(row.get("가격")),
                fulfillment_rate=str(row.get("입고율")),
                major=str(row.get("전공")),
                professor_name=str(row.get("교수명")),
                location=str(row.get("위치")),
                order_date=order_date,
            )

            inserted_id = await BookService.insert_book(book_data=book_data)
            if inserted_id:
                added_books_count += 1

        return total_books_in_file, added_books_count, del_files
