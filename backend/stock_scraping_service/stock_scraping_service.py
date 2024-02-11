import pandas as pd
import time
import requests

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup

from utils.chrome_driver import boot_driver
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


def _get_own_stock_df(driver):
    print("SBI scraping started...")

    # SBI証券のログインページへアクセス
    url_login = "https://site2.sbisec.co.jp/ETGate/"
    driver.get(url_login)
    time.sleep(10)  # ページに遷移する前に次の処理が実行されないようにするため

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
    time.sleep(10)
    print("ログイン完了です")

    # 保有証券一覧ページのリンク
    url_portfolio = "https://site2.sbisec.co.jp/ETGate/?OutSide=on&_ControlID=WPLETacR002Control&_PageID=DefaultPID&_DataStoreID=DSWPLETacR002Control&getFlg=on&_ActionID=DefaultAID&_scpr=intpr%3d230120_dstock_topmypage"
    try:
        driver.get(url_portfolio)
    except:
        print("404")

    time.sleep(5)
    print(driver.page_source.encode("utf-8"))

    csv_link = driver.find_element(By.XPATH, '//a[contains(text(), "CSVダウンロード")]')

    # csv_link = WebDriverWait(driver, 15).until(
    #     EC.element_to_be_clickable(
    #         (By.XPATH, '//a[contains(@href, "CSVダウンロード")]')
    #     )
    # )
    if csv_link is None:
        print("csv_link is None")
    else:
        print(csv_link.text)
    csv_link.click()
    time.sleep(10)
    print("ok")

    # # "もっと見る"ボタンが表示されなくなるまでクリックする
    # while True:
    #     button_element = driver.find_elements(By.CLASS_NAME, "more")
    #     if len(button_element) == 0:
    #         break
    #     button_element[0].click()
    #     time.sleep(3)

    # # ページのhtmlを取得してパースする
    # html = driver.page_source.encode("utf-8")
    # parsed_html = BeautifulSoup(html, "html.parser")

    # # 保有銘柄の証券コード、銘柄名をそれぞれSeriesにする

    # # 証券コード
    # stock_code_list = []
    # tickers = parsed_html.find_all(class_="ticker")

    # for ticker in tickers:
    #     stock_code = ticker.get_text().strip()  # 抽出したテキストに空白がある場合は除去する
    #     stock_code_list.append(stock_code)

    # ser_stock_code = pd.Series(stock_code_list)

    # # 銘柄名
    # stock_name_list = []
    # names = parsed_html.find_all(class_="name")

    # for name in names:
    #     stock_name = name.get_text().strip()  # 抽出したテキストに空白がある場合は除去する
    #     stock_name_list.append(stock_name)

    # ser_stock_name = pd.Series(stock_name_list)

    # # 全銘柄の現在値〜預り区分をデータフレームのリストにする
    # table = parsed_html.find_all("table")
    # list_df_tables = pd.read_html(str(table))

    # # リストのデータフレームを一つに結合する
    # df_all_stock = pd.DataFrame()
    # for df_table in list_df_tables:
    #     row = df_table.T[1:2]
    #     df_all_stock = pd.concat([df_all_stock, row], axis=0)

    # # インデックスを振り直す
    # df_all_stock = df_all_stock.reset_index(drop=True)

    # # 証券コード、銘柄名をデータフレームに結合する
    # df_all_stock = pd.concat([ser_stock_code, ser_stock_name, df_all_stock], axis=1)

    # # カラム名を付け直す
    # df_all_stock.columns = [
    #     "コード",
    #     "名称",
    #     "現在値/前日比",
    #     "保有数量",
    #     "（うち売却注文中）",
    #     "評価損益率",
    #     "平均取得単価",
    #     "預り区分",
    # ]

    # # DBのスキーマに合わせたデータフレームを作成する
    # columns = ["ticker", "name", "quantity", "purchase_price", "current_price"]
    # dtypes = {
    #     "ticker": "object",
    #     "name": "object",
    #     "quantity": "int64",
    #     "purchase_price": "float",
    #     "current_price": "float",
    # }
    # df_own_stock = pd.DataFrame(columns=columns).astype(dtypes)

    # # 整形なしで入れられるデータはそのまま入れる
    # df_own_stock[["ticker", "name"]] = df_all_stock[["コード", "名称"]]

    # # 他のデータは整形して入れる

    # # "3,160円 / -10   -0.32%" → 3160.0
    # df_own_stock["current_price"] = df_all_stock["現在値/前日比"].apply(
    #     lambda x: float(extract_number(x))
    # )

    # # "7 株" → 7
    # df_own_stock["quantity"] = df_all_stock["保有数量"].apply(
    #     lambda x: int(extract_number(x))
    # )

    # # "3,215 円" → 3215
    # df_own_stock["purchase_price"] = df_all_stock["平均取得単価"].apply(
    #     lambda x: int(extract_number(x))
    # )

    # return df_own_stock.to_dict(orient="records")


async def stock_scraping():
    print("boot_driverの実行")
    driver = boot_driver()
    print("boot_driverの完了")
    try:
        _get_own_stock_df(driver)
        # collection_name = "own_stock"
        # # 証券会社のwebサイトから保有株情報を抽出する
        # list_own_stock = _get_own_stock_df(driver)

        # # DBの保有株情報を削除して入れ直す
        # delete_all_documents(collection_name)
        # set_documents(collection_name, list_own_stock)
    except Exception as e:
        print("stock_scrapingでエラーが発生しました", str(e))
    finally:
        if driver is not None:
            driver.quit()
        return "done"


# if __name__ == "__main__":
#     stock_scraping()
