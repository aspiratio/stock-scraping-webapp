import pandas as pd
import gspread
from utils import config
from utils.firestore_utils import get_all_document_values
from google.cloud import secretmanager


def _create_gspread_client():
    # ローカルで動かす時はキーファイルから、Cloud Runで動かす時はシークレットマネージャーから認証情報を取得する
    gspread_client = None
    if config.IS_LOCAL:
        gspread_client = gspread.service_account(config.SERVICE_ACCOUNT_KEY)
    else:
        secret_name = "sa-key-stock-scraping-webapp"
        project_id = config.PROJECT_ID
        client = secretmanager.SecretManagerServiceClient()
        name = client.secret_version_path(project_id, secret_name, "latest")
        secret_version = client.latest_secret_version(name=name)
        key_data = secret_version.payload.data.decode("UTF-8")
        gspread_client = gspread.service_account_from_dict(key_data)
    return gspread_client


async def spreadsheet_update():
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

    # Cloud Runを実行しているサービスアカウントで対象のスプレッドシートにアクセスする
    # 事前にスプレッドシート側で共有設定（サービスアカウントのアドレスを許可）しておく
    gspread_client = _create_gspread_client()
    spreadsheet = gspread_client.open_by_key(config.SPREADSHEET_KEY)

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
