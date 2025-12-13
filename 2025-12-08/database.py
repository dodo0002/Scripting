import sqlite3
# import os


# 資料庫檔案名稱
DB_NAME = "bokelai.db"


def get_db_connection() -> sqlite3.Connection:
    """
    建立並回傳SQLite連線物件
    設定 row_factory 為 sqlite3.Row，使查詢結果可以透過欄位名稱存取
    """
    conn = sqlite3.connect(DB_NAME)

    # print("DB ABS PATH:", os.path.abspath(DB_NAME))

    conn.row_factory = sqlite3.Row
    return conn


# 以下是 CRUD 操作的函式

#  取得全部書籍，按照參數進行分頁
def get_all_books(skip: int, limit: int) -> list[dict]:

    conn = get_db_connection()

    # total = conn.execute("SELECT COUNT(*) FROM books").fetchone()[0]
    # print("TOTAL BOOKS:", total)
    # print("SKIP:", skip, "LIMIT:", limit)

    # 使用 LIMIT 和 OFFSET 進行分頁
    rows = conn.execute(
        "SELECT * FROM books LIMIT ? OFFSET ?",
        (limit, skip)
    ).fetchall()
    conn.close()

    return [dict(row) for row in rows]


#  根據 ID 取得單一書籍資料
def get_book_by_id(book_id: int) -> dict | None:

    conn = get_db_connection()

    row = conn.execute(
        "SELECT * FROM books WHERE id = ?",
        (book_id,)).fetchone()
    conn.close()

    return dict(row) if row else None


# 新增書籍資料
def create_book(title: str,
                author: str,
                publisher: str | None,
                price: int,
                publish_date: str | None,
                isbn: str | None,
                cover_url: str | None) -> int:

    conn = get_db_connection()

    cursor = conn.execute(
        """
        INSERT INTO books (title, author, publisher, price, publish_date, isbn, cover_url)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (title, author, publisher, price, publish_date, isbn, cover_url)
    )

    conn.commit()

    # 取得剛剛新增資料的 ID
    book_id = cursor.lastrowid
    conn.close()

    return book_id


# 完整更新一本書籍資料，回傳是否成功更新
def update_book(book_id: int,
                title: str,
                author: str,
                publisher: str | None,
                price: int,
                publish_date: str | None,
                isbn: str | None,
                cover_url: str | None) -> bool:

    conn = get_db_connection()
    cursor = conn.execute("""
        UPDATE books 
        SET 
            title = ?, 
            author = ?, 
            publisher = ?, 
            price = ?, 
            publish_date = ?, 
            isbn = ?, 
            cover_url = ?
        WHERE id = ?
        """,
                          (title, author, publisher, price,
                           publish_date, isbn, cover_url, book_id)
                          )
    conn.commit()
    conn.close()

    # rowcount > 0 表示有紀錄被更新
    return cursor.rowcount > 0


# 刪除一本書籍資料，回傳是否成功刪除
def delete_book(book_id: int) -> bool:

    conn = get_db_connection()
    cursor = conn.execute("DELETE FROM books WHERE id = ?", (book_id,))
    conn.commit()
    conn.close()

    return cursor.rowcount > 0
