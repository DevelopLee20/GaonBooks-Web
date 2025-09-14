from app.collections.book_collection import BookCollection


# 콜랙션 인덱스 생성 명시
async def create_all_indexes():
    await BookCollection._collection.create_index("book_title")
