from google.cloud import firestore
from utils import config

# 最上流のコレクション名
root_collection_name = config.FIRESTORE_COLLECTION
# 最上流配下のドキュメントID（環境毎にDBを変える場合はここで分ける）
root_doc_id = config.FIRESTORE_DOCUMENT

# Firestoreに接続
db = firestore.Client()
root_doc = db.collection(root_collection_name).document(root_doc_id)


def get_all_document_ids(collection_name: str):
    try:
        # コレクションを取得
        collection = root_doc.collection(collection_name)

        # すべてのドキュメントを取得
        docs = collection.get()

        # ドキュメントIDのみを抽出
        doc_ids = [doc.id for doc in docs]

        return doc_ids

    except Exception:
        raise


def set_documents(collection_name: str, data: dict):
    set_tickers = []
    try:
        for value in data:
            # ドキュメントを指定
            doc_ref = root_doc.collection(collection_name).document(value["ticker"])

            # last_updated_timeフィールドに現在のタイムスタンプを追加
            value["last_updated_time"] = firestore.SERVER_TIMESTAMP

            # 値を追加（既にドキュメントが存在していれば更新）
            doc_ref.set(value)

            set_tickers.append(value["ticker"])

        print(f"{collection_name}にドキュメントの登録が成功しました")
        return set_tickers

    except Exception:
        raise


def delete_all_documents(collection_name: str):
    try:
        # コレクションを取得
        collection = root_doc.collection(collection_name)

        # すべてのドキュメントを取得
        docs = collection.get()

        for doc in docs:
            doc.reference.delete()

        print(f"{collection_name}内のドキュメントを全削除しました")
    except Exception:
        raise
