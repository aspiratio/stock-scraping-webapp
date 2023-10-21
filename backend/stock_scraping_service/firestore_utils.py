from google.cloud import firestore
import config

# 最上流のコレクション名
root_collection_name = config.FIRESTORE_COLLECTION
# 最上流配下のドキュメントID（環境毎にDBを変える場合はここで分ける）
root_doc_id = config.FIRESTORE_DOCUMENT


def get_document_ids(collection_name):
    try:
        # Firestoreに接続
        db = firestore.Client()

        # コレクションを取得（サブコレクションの中に目的のコレクションがある）
        collection = (
            db.collection(root_collection_name)
            .document(root_doc_id)
            .collection(collection_name)
        )

        # すべてのドキュメントを取得
        print(collection)
        docs = collection.get()
        print(docs)

        # ドキュメントIDのみを抽出
        docs_ids = [docs.id for doc in docs]

        return docs_ids

    except Exception as e:
        print(str(e))
