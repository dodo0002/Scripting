import sys
from scraper import scrape_llm_books
from database import setup_db, insert_books, query_books

# 主要為CLI功能


def main_menu():
    setup_db()  # database.py 17

    while True:
        print("-----博客來 LLM 書籍管理系統 -----")
        print("1. 更新書籍資料庫")
        print("2. 查詢書籍")
        print("3. 離開系統")
        print("---------------------------------")

        choice = input("請選擇操作選項 (1-3): ").strip()

        if choice == '1':
            update_data()  # 31
        elif choice == '2':
            query_data()  # 43
        elif choice == '3':
            print("感謝使用！系統已退出。")
            sys.exit(0)
        else:
            print("無效選項，請重新輸入。\n")


def update_data():
    print("開始從網路爬取最新書籍資料...")
    books_data = scrape_llm_books()  # scraper.py 69

    if not books_data:
        print("未獲取任何書籍資料")
        return

    new_records_count = insert_books(books_data)  # database.py 39
    print(f"資料庫更新完成！共爬取 {len(books_data)} 筆資料，新增了{new_records_count}筆新書紀錄\n")


def query_data():

    while True:
        print("\n--- 查詢書籍 ---")
        print("a. 依書名查詢")
        print("b. 依作者查詢")
        print("c. 返回主選單")

        # 去除空白、不區分大小寫
        choice = input("請輸入您的選項 (a/b/c): ").strip().lower()

        if choice == 'c':
            break

        if choice in ('a', 'b'):
            keyword = input("請輸入查詢關鍵字: ").strip()
            if not keyword:
                print("關鍵字不能為空。")
                continue

            if choice == 'a':
                query_type = "title"
            else:
                query_type = "author"

            results = query_books(query_type, keyword)  # database.py 81

            print_book_results(results)  # 76

        else:
            print("無效的選項，請重新輸入。")


def print_book_results(results):

    if not results:
        print("\n查無資料。請嘗試其他關鍵字。")
        return

    print("\n\n====================")
    # 迴圈查詢結果列表
    for i, book in enumerate(results):
        print(f"書名：{book.get('title', 'N/A')}")
        print(f"作者：{book.get('author', 'N/A')}")
        print(f"價格：{book.get('price', 0)}")

        # 判斷是否為最後一本書避免重複顯示結尾
        if i < len(results) - 1:
            print("---")  # 使用 --- 分隔每一本書

    print("====================")


if __name__ == "__main__":
    main_menu()
