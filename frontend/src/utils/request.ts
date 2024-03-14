import axios from "axios"

export const updateStockInfo = async (
  isStock: boolean,
  isDividend: boolean,
  isMarket: boolean,
  isSpreadsheet: boolean
) => {
  await axios
    .get(
      `${process.env.NEXT_PUBLIC_CLOUDRUN_URL}/update_stock_info?stock=${isStock}&dividend=${isDividend}&market=${isMarket}&spreadsheet=${isSpreadsheet}`
    )
    .then((response) => {
      console.log(response.data)
    })
    .catch((error) => {
      alert(error)
    })
}
