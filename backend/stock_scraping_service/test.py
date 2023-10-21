import pandas as pd
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from firestore_utils import get_document_ids
from extract_number import extract_number

import config


def get_own_stock_df():
    return get_document_ids("own_stock")


if __name__ == "__main__":
    # # Chrome オプションの設定
    # chrome_options = Options()
    # chrome_options.add_argument("--headless")  # ヘッドレスモードを有効にする
    # # ドライバーの起動
    # driver = webdriver.Chrome(
    #     service=ChromeService(ChromeDriverManager().install()), options=chrome_options
    # )

    try:
        # 証券会社のwebサイトから保有株情報を抽出する
        df_own_stock = get_own_stock_df()
        print(df_own_stock)
    except Exception as e:
        print("Failed get_own_stock_df")
        print(str(e))
    # finally:
    # driver.quit()
