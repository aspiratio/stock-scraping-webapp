import traceback

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from utils.chrome_driver import boot_driver
from utils.firestore_utils import get_all_document_ids, set_documents
from utils.logger import Logger

logger = Logger()


def _process_stock(driver, ticker):
    print(f"{ticker} start")
    logger.info(f"{ticker} start")
    # 配当ページへアクセス
    url_dividend = f"https://minkabu.jp/stock/{ticker}/dividend"
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
        print(f"{ticker} skipped")
        logger.info(f"{ticker} skipped")
        return 0

    # 1株配当金を取得する
    dividend_integer = dividend_elements[0].text.strip()
    dividend_decimal = dividend_decimal_elements[0].text.strip()
    dividend = float(dividend_integer + dividend_decimal)
    print(f"{ticker} finish")
    logger.info(f"{ticker} finish")
    return dividend


async def dividend_scraping():
    driver = boot_driver()
    try:
        results = []
        input_collection_name = "own_stock"
        output_collection_name = "stock_info"
        tickers = get_all_document_ids(input_collection_name)

        for ticker in tickers:
            dividend = _process_stock(driver, ticker)
            results.append({"ticker": ticker, "dividend_yen": dividend})

        # 結果をDBに登録する
        set_documents(output_collection_name, results)
        return "done"
    except Exception as e:
        print("append_dividendでエラーが発生しました: ", str(e))
        logger.error("append_dividendでエラーが発生しました: ", str(e))
    finally:
        driver.quit()
