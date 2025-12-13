from fastapi import FastAPI, HTTPException, status, Query, Depends
from typing import Annotated
import sqlite3

from database import (
    get_all_books,
    get_book_by_id,
    create_book,
    update_book,
    delete_book
)
from models import BookCreate, BookResponse


app = FastAPI(
    title="AI Books RESTful API",
    description="使用 FastAPI, SQLite, Pydantic 實現的書籍管理 API。",
    version="1.1.0"
)


# 處理404

def get_book_or_404(book_id: int) -> dict:
    """
    根據 ID 嘗試取得書籍資料，若找不到則拋出 404 錯誤。
    """
    book_data = get_book_by_id(book_id)

    if book_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found."
        )
    return book_data


# API 端點

@app.get("/", tags=["Root"])
async def root():
    """API 歡迎訊息"""
    return {"message": "AI Books API"}


@app.get(
    "/books",
    response_model=list[BookResponse],
    tags=["Books"],
    summary="分頁取得書籍列表"
)
async def list_books(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=100)
):
    """
    根據 skip 和 limit 參數分頁取得書籍列表。
    """
    books_data = get_all_books(skip=skip, limit=limit)

    return books_data


@app.get(
    "/books/{book_id}",
    response_model=BookResponse,
    tags=["Books"],
    summary="取得單一書籍資料"
)
async def get_book(book_id: int):
    """
    根據 ID 取得單一書籍資料，找不到回傳404
    """

    book_data = get_book_or_404(book_id)
    return book_data


@app.post(
    "/books",
    response_model=BookResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Books"],
    summary="新增一本書籍"
)
async def create_new_book(book: BookCreate):
    """
    新增一本書籍資料，並回傳新增後的完整資料
    """
    book_data = book.model_dump(exclude_unset=False)

    # 檢查必填欄位
    if not book_data.get('title') or not book_data.get('author') or not book_data.get('price'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing required fields: title, author, and price are necessary for creation."
        )

    new_id = create_book(
        title=book_data['title'],
        author=book_data['author'],
        publisher=book_data.get('publisher'),
        price=book_data['price'],
        publish_date=book_data.get('publish_date'),
        isbn=book_data.get('isbn'),
        cover_url=book_data.get('cover_url')
    )

    return get_book_or_404(new_id)


@app.put(
    "/books/{book_id}",
    response_model=BookResponse,
    tags=["Books"],
    summary="完整更新一本書籍資料"
)
async def update_existing_book(book_id: int, book: BookCreate):
    """
    完整更新指定 ID 的書籍資料，找不到回傳 404
    """
    get_book_or_404(book_id)

    book_data = book.model_dump(exclude_unset=False)

    # 檢查必填欄位
    if not book_data.get('title') or not book_data.get('author') or not book_data.get('price'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing required fields: title, author, and price cannot be empty during PUT update."
        )

    success = update_book(
        book_id=book_id,
        title=book_data['title'],
        author=book_data['author'],
        publisher=book_data.get('publisher'),
        price=book_data['price'],
        publish_date=book_data.get('publish_date'),
        isbn=book_data.get('isbn'),
        cover_url=book_data.get('cover_url')
    )

    if not success:
        pass

    return get_book_or_404(book_id)


@app.delete(
    "/books/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Books"],
    summary="刪除一本書籍資料"
)
async def delete_existing_book(book_id: int):
    """
    根據 ID 刪除書籍資料，成功不回傳內容
    """
    success = delete_book(book_id)

    # 檢查是否有記錄被刪除
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found."
        )

    return
