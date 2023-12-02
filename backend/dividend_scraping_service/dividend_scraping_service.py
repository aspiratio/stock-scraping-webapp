import concurrent.futures
import traceback

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from utils.chrome_driver import boot_driver
from utils.firestore_utils import get_all_document_ids, set_documents


def _process_stock(stock_code):
    print(f"{stock_code} start")
    try:
        driver = boot_driver()
        # 配当ページへアクセス
        url_dividend = f"https://minkabu.jp/stock/{stock_code}/dividend"
        driver.get(url_dividend)

        # 要素が表示されるまで待機する
        wait = WebDriverWait(driver, 10)
        try:
            dividend_elements = wait.until(
                EC.visibility_of_all_elements_located(
                    (By.CLASS_NAME, "dividend-state__amount__integer")
                )
            )
            dividend_decimal_elements = wait.until(
                EC.visibility_of_all_elements_located(
                    (By.CLASS_NAME, "dividend-state__amount__decimal")
                )
            )
        except TimeoutException:
            # 予想配当金がないものは0円として処理する
            print(f"{stock_code} skipped")
            return stock_code, 0

        # 1株配当金を取得する
        dividend_integer = dividend_elements[0].text.strip()
        dividend_decimal = dividend_decimal_elements[0].text.strip()
        dividend = float(dividend_integer + dividend_decimal)
        print(f"{stock_code} finish")
        return stock_code, dividend
    finally:
        driver.quit()


def dividend_scraping():
    try:
        results = {}
        collection_name = "stock_stock"
        stock_codes = get_all_document_ids(collection_name)
        with concurrent.futures.ProcessPoolExecutor(max_workers=5) as executor:
            futures = [
                executor.submit(_process_stock, stock_code)
                for stock_code in stock_codes
            ]

            for future in concurrent.futures.as_completed(futures):
                stock_code, dividend = future.result()
                results[stock_code] = dividend

        # 結果をDBに登録する
        for stock_code, dividend in results:
            set_documents(collection_name, results)
        return "done"
    except Exception as e:
        print("append_dividendでエラーが発生しました: ", str(e))
        traceback.print_exc()
