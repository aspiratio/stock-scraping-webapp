import pandas as pd
import gspread
from utils import config
from utils.firestore_utils import get_all_document_values


async def spreadsheet_update():
    try:
        # それぞれDBから取得したリストをデータフレームに変換する
        own_stock_list = get_all_document_values("own_stock")
        own_stock_df = pd.DataFrame(own_stock_list)

        stock_info_list = get_all_document_values("stock_info")
        stock_info_df = pd.DataFrame(stock_info_list)

        print("DBからデータを取得しました")

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

        # ローカルで動かす時だけキーファイルのパスを指定する必要がある
        key_path = None
        if config.SERVICE_ACCOUNT_KEY:
            key_path = config.SERVICE_ACCOUNT_KEY

        # Cloud Runを実行しているサービスアカウントで対象のスプレッドシートにアクセスする
        # 事前にスプレッドシート側で共有設定（サービスアカウントのアドレスを許可）しておく
        gc = gspread.service_account(key_path)
        spreadsheet = gc.open_by_key(config.SPREADSHEET_KEY)

        # シート名を指定してシートを開く
        worksheet = spreadsheet.worksheet(config.SHEET_NAME)
        print("シートを開きました")

        # シートの既存の値をクリアする（B列からJ列だけ上書きするため）
        worksheet.batch_clear(["B4:I300"])

        # シートのB4:J4からデータフレームの値を書き込む
        cell_range = f"B4:I{3 + len(stock_list)}"
        worksheet.update(cell_range, stock_list)

        print("値を更新しました")
        return "done"
    except Exception as e:
        print("spreadsheet_updateでエラーが発生しました: ", str(e))
