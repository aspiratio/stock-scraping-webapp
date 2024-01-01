"use client"
import axios from "axios"
import Button from "@/components/button"
import { useState } from "react"

const Home = () => {
  const [isStock, setIsStock] = useState<boolean>(false)
  const [isDividend, setIsDividend] = useState<boolean>(false)
  const [isMarket, setIsMarket] = useState<boolean>(false)
  const [isSpreadsheet, setIsSpreadsheet] = useState<boolean>(false)

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()

    // それぞれのチェックボックスの状態をログに出力
    console.log("isStock:", isStock)
    console.log("isDividend:", isDividend)
    console.log("isMarket:", isMarket)
    console.log("isSpreadsheet:", isSpreadsheet)
    axios
      .get(
        `https://stock-scraping-service-bp6w7fuqsq-an.a.run.app/update_stock_info?stock=${isStock}&dividend=${isDividend}&market=${isMarket}&spreadsheet=${isSpreadsheet}`
      )
      .then((response) => {
        console.log(response.data)
      })
      .catch((error) => {
        console.error(error)
      })
  }
  return (
    <form
      onSubmit={(e) => handleSubmit(e)}
      className="text-lg flex flex-col justify-center h-screen w-1/2 mx-auto"
    >
      <div>
        <input
          type="checkbox"
          id="stock"
          className="mr-2"
          checked={isStock}
          onChange={(e) => setIsStock(e.target.checked)}
        />
        <label htmlFor="stock">保有株情報</label>
      </div>
      <div>
        <input
          type="checkbox"
          id="dividend"
          className="mr-2"
          checked={isDividend}
          onChange={(e) => setIsDividend(e.target.checked)}
        />
        <label htmlFor="dividend">配当金情報</label>
      </div>
      <div>
        <input
          type="checkbox"
          id="market"
          className="mr-2"
          checked={isMarket}
          onChange={(e) => setIsMarket(e.target.checked)}
        />
        <label htmlFor="market">業種情報</label>
      </div>
      <div>
        <input
          type="checkbox"
          id="spreadsheet"
          className="mr-2"
          checked={isSpreadsheet}
          onChange={(e) => setIsSpreadsheet(e.target.checked)}
        />
        <label htmlFor="spreadsheet">スプレッドシート</label>
      </div>
      <Button type="submit" className="mt-8">
        送信
      </Button>
    </form>
  )
}

export default Home
