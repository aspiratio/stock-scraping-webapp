import pandas as pd
from utils.firestore_utils import get_all_document_values


async def spreadsheet_update():
    # それぞれDBから取得したリストをデータフレームに変換する
    own_stock_list = get_all_document_values("own_stock")
    own_stock_df = pd.DataFrame(own_stock_list)

    stock_info_list = get_all_document_values("stock_info")
    stock_info_df = pd.DataFrame(stock_info_list)

    # 企業コードでJOINする
    stock_merged_df = pd.merge(own_stock_df, stock_info_df, on="ticker", how="left")

    # スプレッドシートの列の並び
    columns_order = [
        "ticker",
        "market",
        "name",
        "industries",
        "quantity",
        "purchase_price",
        "current_price",
        "dividend_yen",
    ]

    # データフレームから必要な列だけ取り出し、かつ並び替える
    stock_merged_df_selected = stock_merged_df.loc[:, columns_order][columns_order]

    # スプレッドシートに書き込めるようにリスト形式に変換する
    stock_list = stock_merged_df_selected.values.tolist()

    print(stock_list)

    # # 2つのAPIを記述しないとリフレッシュトークンを3600秒毎に発行し続けなければならない
    # scope = [
    #     "https://spreadsheets.google.com/feeds",
    #     "https://www.googleapis.com/auth/drive",
    # ]

    # # 認証情報設定
    # credentials = ServiceAccountCredentials.from_json_keyfile_name(
    #     "keys/credentials.json", scope
    # )

    # # OAuth2の資格情報を使用してGoogle APIにログイン
    # gc = gspread.authorize(credentials)

    # # 共有設定したスプレッドシートを開く
    # spreadsheet = gc.open_by_key(config.SPREADSHEET_KEY)

    # # シート名を指定してシートを開く
    # worksheet = spreadsheet.worksheet(config.SHEET_NAME)

    # # シートの既存の値をクリアする（B列からJ列だけ上書きするため）
    # worksheet.batch_clear(["B4:I300"])

    # # シートのB4:J4からデータフレームの値を書き込む
    # cell_range = f"B4:I{3 + len(list_own_stock)}"
    # worksheet.update(cell_range, list_own_stock)
    return "done"
