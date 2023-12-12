# 環境変数を取得する
import os
import json
from dotenv import load_dotenv, find_dotenv

# ローカルの .env ファイルをロードする
load_dotenv(find_dotenv())

# Cloud Run の環境変数を取得する
# ローカルには ACCOUNT_INFO の環境変数はないため、None になる。その時だけローカルの環境変数を利用する
secret_key_json = os.getenv("ACCOUNT_INFO")
sbi_username = ""
sbi_password = ""
spreadsheet_key = ""

if secret_key_json is None:
    sbi_username = os.getenv("SBI_USERNAME")
    sbi_password = os.getenv("SBI_PASSWORD")
    spreadsheet_key = os.getenv("SPREADSHEET_KEY")
else:
    sbi_username = json.loads(secret_key_json)["SBI_USERNAME"]
    sbi_password = json.loads(secret_key_json)["SBI_PASSWORD"]
    spreadsheet_key = json.loads(secret_key_json)["SPREADSHEET_KEY"]


SBI_USERNAME = sbi_username
SBI_PASSWORD = sbi_password
SPREADSHEET_KEY = spreadsheet_key

SHEET_NAME = os.getenv("SHEET_NAME")
FIRESTORE_COLLECTION = os.getenv("FIRESTORE_COLLECTION")
FIRESTORE_DOCUMENT = os.getenv("FIRESTORE_DOCUMENT")
SERVICE_ACCOUNT_KEY = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
