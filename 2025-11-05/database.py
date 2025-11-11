import sqlite3

# 用來寫入資料庫


DB_NAME = "books.db"
TABLE_NAME = "llm_books"


def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    # sqlite3.Row物件可以增加調用tuple索引的方式
    conn.row_factory = sqlite3.Row
    return conn


def setup_db():
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()

            # SQLite與oracle的不同，型別上的限制較為不嚴格
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL UNIQUE,
                    author TEXT,
                    price INTEGER,
                    link TEXT
                );
            """)
            # 跟SQL developer 上方工具列的小勾勾相同功能
            conn.commit()

    except sqlite3.Error as e:
        print(f"資料庫初始化錯誤: {e}")


def insert_books(books):
    if not books:
        return 0

# 用佔位符防止注入
    insert_sql = f"""
        INSERT OR IGNORE INTO {TABLE_NAME} (title, author, price, link)
        VALUES (?, ?, ?, ?);
    """

    data_insert = []
    for book in books:
        data_insert.append((
            book.get('title', 'N/A'),
            book.get('author', 'N/A'),
            book.get('price', 0),
            book.get('link', 'N/A')
        ))

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}")
            # 初始筆數
            initial_count = cursor.fetchone()[0]
            # 批量插入
            cursor.executemany(insert_sql, data_insert)  # 38, 43
            conn.commit()
            # 插入後最終筆數
            cursor.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}")
            final_count = cursor.fetchone()[0]

            # 相減得到差異筆數
            new_records = final_count - initial_count
            return new_records

    except sqlite3.Error as e:
        print(f"資料庫插入錯誤: {e}")
        return 0


def query_books(query_type, keyword):

    # 進行模糊比對
    sql_query = f"SELECT * FROM {TABLE_NAME} WHERE {query_type} LIKE ?;"
    # sqlite3模組寫法，會自動將like_keyword帶入sql_query中結尾的 ? 用途是防止注入
    like_keyword = f"%{keyword}%"

    results = []

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()

            # 第二個參數為tuple
            cursor.execute(sql_query, (like_keyword,))

            for row in cursor.fetchall():
                # 將 sqlite3.Row 轉換為標準字典
                results.append(dict(row))

    except sqlite3.Error as e:
        print(f"資料庫查詢錯誤: {e}")

    return results


# 以下是測試範例，為避免誤觸所以註解
# if __name__ == '__main__':
#     setup_db()
    # 示範插入
    # print(insert_books([
    #     {"title": "測試書名 1", "author": "測試作者", "price": 100, "link": "http://test.link"},
    # ]))
    # 示範查詢
    # results = query_books("author", "測試")
    # print(results)
