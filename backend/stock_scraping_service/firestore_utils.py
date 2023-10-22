from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter
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

        print("ドキュメントの登録に成功しました")
        return set_tickers

    except Exception:
        raise


def delete_documents_except_tickers(collection_name: str, tickers: list):
    """
    指定したtickerを持つドキュメント以外を削除する
    """
    ref = root_doc.collection(collection_name)
    try:
        docs_to_delete = ref.where(
            filter=FieldFilter("ticker", "not-in", tickers)
        ).get()

        print(docs_to_delete)

        for doc in docs_to_delete:
            print(doc.reference)
            doc.reference.delete()
        print("ドキュメントの削除に成功しました")
    except Exception:
        print("ドキュメントの削除に失敗しました")
        raise
