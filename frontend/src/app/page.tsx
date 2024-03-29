"use client"
import Button from "@/components/button"
import { useState } from "react"
import { updateStockInfo } from "@/utils/request"
import ConfirmDialog from "@/components/dialog"
import Loading from "@/components/loading"
import { useFirestoreSubscription } from "@/utils/hooks/useFirestoreSubscription"

const Home = () => {
  const [isStock, setIsStock] = useState<boolean>(false)
  const [isDividend, setIsDividend] = useState<boolean>(false)
  const [isMarket, setIsMarket] = useState<boolean>(false)
  const [isSpreadsheet, setIsSpreadsheet] = useState<boolean>(false)
  const [isDialogOpen, setIsDialogOpen] = useState<boolean>(false)
  const [isLoading, setIsLoading] = useState<boolean>(false)

  const { ownStockData, stockInfoData } = useFirestoreSubscription()

  const handleDialogOpen = () => {
    setIsDialogOpen(!isDialogOpen)
  }

  const submitRequest = async () => {
    setIsLoading(true)
    handleDialogOpen()
    await updateStockInfo(isStock, isDividend, isMarket, isSpreadsheet)
    setIsLoading(false)
  }

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    handleDialogOpen()
  }

  return (
    <>
      {isDialogOpen && (
        <ConfirmDialog
          isOpen={isDialogOpen}
          handleOpen={handleDialogOpen}
          onClickSubmit={submitRequest}
        >
          送信しますか？
        </ConfirmDialog>
      )}
      <form
        onSubmit={(e) => handleSubmit(e)}
        className="text-xl flex flex-col justify-center h-screen w-3/4 max-w-md mx-auto gap-2"
      >
        <div>
          <input
            type="checkbox"
            id="stock"
            className="mr-2 size-4"
            checked={isStock}
            onChange={(e) => setIsStock(e.target.checked)}
          />
          <label htmlFor="stock">
            保有株情報
            <span className="block text-base ml-6">
              {ownStockData?.last_updated_time.toDate().toLocaleString()}
            </span>
          </label>
        </div>
        <div>
          <input
            type="checkbox"
            id="dividend"
            className="mr-2 size-4"
            checked={isDividend}
            onChange={(e) => setIsDividend(e.target.checked)}
          />
          <label htmlFor="dividend">
            配当金情報
            <span className="block text-base ml-6">
              {stockInfoData?.last_updated_time.toDate().toLocaleString()}
            </span>
          </label>
        </div>
        <div>
          <input
            type="checkbox"
            id="market"
            className="mr-2 size-4"
            checked={isMarket}
            onChange={(e) => setIsMarket(e.target.checked)}
          />
          <label htmlFor="market">
            業種情報
            <span className="block text-base ml-6">
              {stockInfoData?.last_updated_time.toDate().toLocaleString()}
            </span>
          </label>
        </div>
        <div>
          <input
            type="checkbox"
            id="spreadsheet"
            className="mr-2 size-4"
            checked={isSpreadsheet}
            onChange={(e) => setIsSpreadsheet(e.target.checked)}
          />
          <label htmlFor="spreadsheet">スプレッドシート</label>
        </div>
        {isLoading ? (
          <Loading />
        ) : (
          <Button type="submit" className="mt-8">
            送信
          </Button>
        )}
      </form>
    </>
  )
}

export default Home
