import os
import pandas as pd
import time
from io import StringIO
import requests

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup

from utils.chrome_driver import boot_driver, boot_driver_venv
from utils.firestore_utils import (
    set_documents,
    delete_all_documents,
)
from utils import config

import re


def extract_number(text):
    """
    文字列から数値部分のみを抽出するための関数
    """
    number = re.findall(r"[-+]?\d*\.\d+|\d+", text.replace(",", ""))[0]
    return number


def _get_own_stock_df(driver, file_directory):
    print("SBI scraping started...")

    # SBI証券のログインページへアクセス
    url_login = "https://site2.sbisec.co.jp/ETGate/"
    driver.get(url_login)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "user_id"))
    )  # ログインページが表示されるまで最大10秒待つ

    username = driver.find_element(By.NAME, "user_id")
    password = driver.find_element(By.NAME, "user_password")
    login_btn = driver.find_element(By.NAME, "ACT_login")

    # 念のためテキストボックスの中身を空にする
    username.clear()
    password.clear()

    # テキストボックスに値を入力する
    username.send_keys(config.SBI_USERNAME)
    password.send_keys(config.SBI_PASSWORD)

    # ログインボタンをクリックする
    login_btn.click()
    # ログインが完了するのを待つ
    time.sleep(10)

    # 保有証券一覧ページのリンク
    url_portfolio = "https://site2.sbisec.co.jp/ETGate/?OutSide=on&_ControlID=WPLETacR002Control&_PageID=DefaultPID&_DataStoreID=DSWPLETacR002Control&getFlg=on&_ActionID=DefaultAID&_scpr=intpr%3d230120_dstock_topmypage"

    # CSVダウンロードリンクが表示されるまで最大10秒待つ
    driver.get(url_portfolio)
    csv_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, '//a[contains(text(), "CSVダウンロード")]')
        )
    )
    csv_link.click()

    # ダウンロードが完了するのを待つ
    time.sleep(10)

    downloaded_csv_path = file_directory + "/SaveFile.csv"

    # 複数回実行したときに名前が重複しないようにリネームする
    renamed_csv_path = (
        file_directory + "/own_stock_" + time.strftime("%Y%m%d%H%M%S") + ".csv"
    )
    os.rename(downloaded_csv_path, renamed_csv_path)

    # データフレーム化できるようにCSVを加工する
    with open(renamed_csv_path, "r", encoding="shift-jis") as file:
        content = file.read()
        start_line = content.find(
            "銘柄コード,銘柄名称,保有株数"
        )  # この行がヘッダーになる
        end_line = (
            content.find("投資信託（金額/特定預り）合計") - 2
        )  # この行より後ろは不要

    data = StringIO(content[start_line:end_line])
    df_own_stock = pd.read_csv(data)

    # 必要な列のみを抽出する
    df_own_stock = df_own_stock[
        ["銘柄コード", "銘柄名称", "保有株数", "取得単価", "現在値"]
    ]

    replaced_columns = {
        "銘柄コード": "ticker",
        "銘柄名称": "name",
        "保有株数": "quantity",
        "取得単価": "purchase_price",
        "現在値": "current_price",
    }

    dtypes = {
        "ticker": "str",
        "name": "str",
        "quantity": "int64",
        "purchase_price": "float",
        "current_price": "float",
    }

    # カラム名とデータ型を変更
    df_own_stock = df_own_stock.rename(columns=replaced_columns).astype(dtypes)

    return df_own_stock.to_dict(orient="records")


async def stock_scraping():
    # 実行された.pyファイルが存在するディレクトリを取得
    file_directory = os.path.dirname(os.path.abspath(__file__))
    print("boot_driverの実行")
    driver = boot_driver(file_directory)
    print("boot_driverの完了")
    try:
        collection_name = "own_stock"
        # 証券会社のwebサイトから保有株情報を抽出する
        list_own_stock = _get_own_stock_df(driver, file_directory)

        # DBの保有株情報を削除して入れ直す
        delete_all_documents(collection_name)
        set_documents(collection_name, list_own_stock)
    except Exception as e:
        print("stock_scrapingでエラーが発生しました", str(e))
    finally:
        if driver is not None:
            driver.quit()
        return "done"


# ローカル環境でのテスト実行用
def stock_scraping_local():
    # このファイルが存在するディレクトリを取得（ここにCSVをダウンロードする）
    file_directory = os.path.dirname(os.path.abspath(__file__))
    print("boot_driverの実行")
    driver = boot_driver_venv(file_directory)
    print("boot_driverの完了")
    try:
        collection_name = "own_stock"
        # 証券会社のwebサイトから保有株情報を抽出する
        list_own_stock = _get_own_stock_df(driver, file_directory)

        # DBの保有株情報を削除して入れ直す
        delete_all_documents(collection_name)
        set_documents(collection_name, list_own_stock)
    except Exception as e:
        print("stock_scrapingでエラーが発生しました", str(e))
    finally:
        if driver is not None:
            driver.quit()


if __name__ == "__main__":
    stock_scraping_local()
