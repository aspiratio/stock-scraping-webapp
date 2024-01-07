from fastapi import FastAPI
import asyncio
from stock_scraping_service import stock_scraping_service
from dividend_scraping_service import dividend_scraping_service
from spreadsheet_update_service import spreadsheet_update_service
from market_update_service import market_update_service
from utils.logger import Logger
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
logger = Logger()

# 許可するオリジン TODO:本番のホスティング後に本番のオリジンを追加する
origins = ["http://localhost:3000"]

# CORSエラーを防ぐためのミドルウェアを追加する
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 指定したオリジンのみ許可
    allow_credentials=True,
    allow_methods=["GET"],  # GETメソッドだけ許可
    allow_headers=["*"],  # すべてのヘッダーを許可
)


async def async_update_stock_info(
    stock: bool, dividend: bool, market: bool, spreadsheet: bool
):
    if stock:
        print("stock_scraping: start")
        await stock_scraping_service.stock_scraping()
        print("stock_scraping: done")

    if dividend:
        print("dividend_scraping: start")
        await dividend_scraping_service.dividend_scraping()
        print("dividend_scraping: done")

    if market:
        print("market_update_service: start")
        await market_update_service.update_market_and_industries()
        print("market_update_service: done")

    if spreadsheet:
        print("spreadsheet_update: start")
        await spreadsheet_update_service.spreadsheet_update()
        print("spreadsheet_update: done")


@app.get("/update_stock_info")
async def update_stock_info(
    stock: bool = True,
    dividend: bool = True,
    market: bool = True,
    spreadsheet: bool = True,
):
    print("リクエストを受け付けました")
    try:
        print(
            f"stock: {stock}, dividend: {dividend}, market: {market}, spreadsheet: {spreadsheet}"
        )
        asyncio.create_task(
            async_update_stock_info(stock, dividend, market, spreadsheet)
        )
        return {"message": "保有株情報を更新中です"}
    except Exception as e:
        print("error_message: ", e)
        return {"message": "エラーです"}
