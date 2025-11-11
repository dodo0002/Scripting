import re
from selenium import webdriver
from selenium.webdriver.common.by import By  # selenium4一定要使用
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# 用來爬蟲

# 爬取博客來書店網頁網址

BKL_URL = "https://search.books.com.tw/search/query/key/LLM/cat/BKA/page/1"


# 將資料清洗成純數字
def price(price_str):
    # 擷取數字部分
    numbers = re.findall(r'\d+', price_str)
    # 找不到標價則返回0
    if numbers:
        return int(numbers[-1])
    else:
        return 0


def extract_book_data(book_element):
    book_info = {
        'title': 'N/A',
        'author': 'N/A',
        'price': 0,
        'link': 'N/A'
    }

    # 避免書籍資訊不完整導致遺漏，分成三段

    try:
        # 擷取書名和連結
        title_element = book_element.find_element(By.CSS_SELECTOR, 'h4>a')
        book_info['title'] = title_element.text.strip()
        book_info['link'] = title_element.get_attribute('href')
    except Exception:
        pass

    try:
        # 擷取作者
        author_element = book_element.find_elements(
            By.CSS_SELECTOR, 'p.author a')
        if author_element:
            authors = []
            for a in author_element:
                clear_author_name = a.text.strip()
                authors.append(clear_author_name)

            book_info['author'] = ", ".join(authors)
    except Exception:
        pass

    try:
        #  擷取價格
        price_element = book_element.find_element(By.CSS_SELECTOR, 'ul.price')
        book_info['price'] = price(
            price_element.get_attribute('innerHTML'))  # 16
    except Exception:
        pass

    return book_info


def scrape_llm_books():

    all_books = []

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36")

    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(BKL_URL)
        wait = WebDriverWait(driver, 20)  # 最多等待20秒

        page_num = 1

        select_element = driver.find_element(By.ID, 'page_select')
        # select裡面的option總共有總頁次 +1個，所以要減一才是正確的總頁次
        total_pages = len(select_element.find_elements(
            By.TAG_NAME, 'option'))-1
        print(f"偵測到總共有{total_pages}頁")

        while True:

            print(f"正在爬取第 {page_num} / {total_pages} 頁..")
            wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'div.table-searchbox')))

            book_elements = driver.find_elements(
                By.CSS_SELECTOR, 'div.table-searchbox div.table-tr:nth-child(1) div.table-td')

            if not book_elements:
                print("找不到書籍資料，爬蟲結束。")
                break

            for element in book_elements:
                data = extract_book_data(element)
                if data['title'] != 'N/A':
                    all_books.append(data)

            try:
                # 下一頁的tag
                next_page_link = wait.until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, 'a.next')
                    )
                )

                # 檢查是否為最後一頁
                last_href = next_page_link.get_attribute('href')
                if last_href is None or last_href == "" or "javascript" in last_href:
                    print("已爬取完成，結束爬蟲。")
                    break

                # 點擊
                next_page_link.click()
                page_num += 1

                # 在點擊後增加延遲，確保頁面有時間載入內容
                time.sleep(3)

            except Exception:
                print(Exception)

        return all_books

    except Exception as e:
        print(f"爬蟲錯誤: {e}")
        # 返回空列表
        return []


if __name__ == '__main__':
    # 示範爬蟲
    books = scrape_llm_books()

    if books:
        print("--- 總結 ---")
        print(f"總共爬取到 {len(books)} 筆資料。")
    else:
        print("--- 總結 ---")
        print("未抓取到任何資料。")
