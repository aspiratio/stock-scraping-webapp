import { useEffect, useState } from "react"
import { OwnStock, StockInfo, firestorePathService } from "../firestore"
import { limit, onSnapshot, orderBy, query } from "firebase/firestore"

export const useFirestoreSubscription = () => {
  const [ownStockData, setOwnStockData] = useState<OwnStock>()
  const [stockInfoData, setStockInfoData] = useState<StockInfo>()

  useEffect(() => {
    const latestOwnStockDoc = query(
      firestorePathService.ownStocks(),
      orderBy("last_updated_time", "desc"),
      limit(1)
    )
    const unsubscribeOwnStock = onSnapshot(latestOwnStockDoc, (snapshot) => {
      snapshot.docs.forEach((doc) => {
        setOwnStockData(doc.data() as OwnStock)
      })
    })

    const latestStockInfoDoc = query(
      firestorePathService.stockInfos(),
      orderBy("last_updated_time", "desc"),
      limit(1)
    )
    const unsubscribeStockInfo = onSnapshot(latestStockInfoDoc, (snapshot) => {
      snapshot.docs.forEach((doc) => {
        setStockInfoData(doc.data() as StockInfo)
      })
    })

    return () => {
      unsubscribeOwnStock()
      unsubscribeStockInfo()
    }
  }, [])

  return { ownStockData, stockInfoData }
}
