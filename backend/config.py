# TODO: Cloud Run上で動すときは Secret Manager から認証情報を持ってくるようにする
# .env ファイルをロードして環境変数へ反映
from dotenv import load_dotenv

load_dotenv()

# 環境変数を参照
import os

SBI_USERNAME = os.getenv("SBI_USERNAME")
SBI_PASSWORD = os.getenv("SBI_PASSWORD")
SPREADSHEET_KEY = os.getenv("SPREADSHEET_KEY")
SHEET_NAME = os.getenv("SHEET_NAME")

print(SBI_USERNAME)
