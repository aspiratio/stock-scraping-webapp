from fastapi import FastAPI
import asyncio
from stock_scraping_service import stock_scraping_service
from dividend_scraping_service import dividend_scraping_service
from spreadsheet_update_service import spreadsheet_update_service
from utils.chrome_driver import boot_driver

app = FastAPI()


async def async_update_stock_info(stock: bool, dividend: bool, spreadsheet: bool):
    tasks = []

    if stock:
        print("stock_scraping: start")
        tasks.append(stock_scraping_service.stock_scraping())
        print("stock_scraping: done")

    if dividend:
        print("dividend_scraping: start")
        tasks.append(dividend_scraping_service.dividend_scraping())
        print("dividend_scraping: done")

    if spreadsheet:
        print("spreadsheet_update: start")
        tasks.append(spreadsheet_update_service.spreadsheet_update())
        print("spreadsheet_update: done")

    await asyncio.gather(*tasks)


@app.get("/update_stock_info")
async def update_stock_info(
    stock: bool = True, dividend: bool = True, spreadsheet: bool = True
):
    try:
        asyncio.create_task(async_update_stock_info(stock, dividend, spreadsheet))
        return {"message": "保有株情報を更新中です"}
    except Exception as e:
        print("error_message: ", e)
        return {"message": "エラーです"}
