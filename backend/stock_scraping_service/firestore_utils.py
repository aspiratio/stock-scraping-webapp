import json
from google.cloud import firestore
import config

# 最上流のコレクション名
root_collection_name = config.FIRESTORE_COLLECTION
# 最上流配下のドキュメントID（環境毎にDBを変える場合はここで分ける）
root_doc_id = config.FIRESTORE_DOCUMENT

# Firestoreに接続
db = firestore.Client()
root_doc = db.collection(root_collection_name).document(root_doc_id)


def get_document_ids(collection_name: str):
    try:
        # コレクションを取得
        collection = root_doc.collection(collection_name)

        # すべてのドキュメントを取得
        docs = collection.get()

        # ドキュメントIDのみを抽出
        doc_ids = [doc.id for doc in docs]

        return doc_ids

    except Exception as e:
        print(str(e))


def set_documents(collection_name: str, json_values: json):
    values = json.loads(json_values)
    try:
        for value in values:
            print(value)
            # ドキュメントを指定
            # doc_ref = root_doc.collection(collection_name).document(value.ticker)
            # doc_

    except Exception as e:
        print(str(e))
