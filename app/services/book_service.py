from typing import List

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
        return await BookCollection.soft_delete_book_by_id(id=book_id)

    @classmethod
    async def select_books_by_title(cls, book_title: str) -> List[BookDocument]:
        books = await BookCollection.select_book_by_book_title(book_title=book_title)

        return books
