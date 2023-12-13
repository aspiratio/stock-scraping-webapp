# 環境変数を取得する
import os
import json
from dotenv import load_dotenv, find_dotenv

# ローカルの .env ファイルをロードする
load_dotenv(find_dotenv())

environment = os.getenv("ENVIRONMENT")
sbi_username = ""
sbi_password = ""
spreadsheet_key = ""

# ローカルならenvファイルから環境変数の値を取得する
if environment == "local":
    sbi_username = os.getenv("SBI_USERNAME")
    sbi_password = os.getenv("SBI_PASSWORD")
    spreadsheet_key = os.getenv("SPREADSHEET_KEY")
else:
    secret_key_json = os.getenv("ACCOUNT_INFO")
    project_id = os.getenv("PROJECT_ID")
    sbi_username = json.loads(secret_key_json)["SBI_USERNAME"]
    sbi_password = json.loads(secret_key_json)["SBI_PASSWORD"]
    spreadsheet_key = json.loads(secret_key_json)["SPREADSHEET_KEY"]

IS_LOCAL = environment == "local"
PROJECT_ID = project_id
SBI_USERNAME = sbi_username
SBI_PASSWORD = sbi_password
SPREADSHEET_KEY = spreadsheet_key

SHEET_NAME = os.getenv("SHEET_NAME")
FIRESTORE_COLLECTION = os.getenv("FIRESTORE_COLLECTION")
FIRESTORE_DOCUMENT = os.getenv("FIRESTORE_DOCUMENT")
SERVICE_ACCOUNT_KEY = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
