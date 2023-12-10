import pandas as pd
import requests

from utils.firestore_utils import get_all_document_ids, update_documents


def _get_tse_stock_df():
    stock_list_url = "https://www.jpx.co.jp/markets/statistics-equities/misc/tvdivq0000001vg2-att/data_j.xls"
    response = requests.get(stock_list_url)
    return pd.read_excel(response.content)


async def update_market_and_industries():
    df_tse_stock = _get_tse_stock_df()

    tickers = get_all_document_ids("stock_info")

    # 企業コードが数値のため、文字列に変える（TODO: 元データが文字列に変わればこの記述は消す）
    df_tse_stock["コード"] = df_tse_stock["コード"].astype(str)

    df_own_stock = df_tse_stock[df_tse_stock["コード"].isin(tickers)].loc[
        :, ["コード", "市場・商品区分", "33業種区分"]
    ]

    # DBのフィールド名に合わせたカラム名に付け直す
    df_own_stock.columns = ["ticker", "market", "industries"]

    # DBに登録するためにリスト型に変換する
    list_own_stock = df_own_stock.to_dict(orient="records")

    update_documents("stock_info", list_own_stock)

    return "done"
