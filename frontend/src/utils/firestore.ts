import { db } from "@/utils/config"
import {
  CollectionReference,
  DocumentReference,
  Timestamp,
  collection,
  doc,
} from "firebase/firestore"

type OwnStock = {
  current_price: number
  last_updated_time: Timestamp
  name: string
  purchase_price: number
  quantity: number
  ticker: string
}

type StockInfo = {
  dividend_yen: number
  industries: string
  last_updated_time: Timestamp
  market: string
  ticker: string
}

class FirestorePathService {
  private root_collection_name = process.env.NEXT_PUBLIC_FIRESTORE_COLLECTION //最上流のコレクション名
  private root_doc_id = process.env.NEXT_PUBLIC_FIRESTORE_DOCUMENT // 最上流配下のドキュメントID（環境毎にDBを変える場合はここで分ける）
  public root_doc // サブコレクション

  constructor() {
    if (
      !process.env.NEXT_PUBLIC_FIRESTORE_COLLECTION ||
      !process.env.NEXT_PUBLIC_FIRESTORE_DOCUMENT
    ) {
      throw new Error("環境変数が設定されていません。")
    }

    this.root_collection_name = process.env.NEXT_PUBLIC_FIRESTORE_COLLECTION
    this.root_doc_id = process.env.NEXT_PUBLIC_FIRESTORE_DOCUMENT
    this.root_doc = doc(db, this.root_collection_name, this.root_doc_id)
  }

  public ownStocks = () =>
    collection(this.root_doc, "own_stock") as CollectionReference<OwnStock>
  public ownStock = (id: string) =>
    doc(this.root_doc, "own_stock", id) as DocumentReference<OwnStock>

  public stockInfos = () =>
    collection(this.root_doc, "stock_info") as CollectionReference<StockInfo>
  public stockInfo = (id: string) =>
    doc(this.root_doc, "stock_info", id) as DocumentReference<StockInfo>
}

export const firestorePathService = new FirestorePathService()
