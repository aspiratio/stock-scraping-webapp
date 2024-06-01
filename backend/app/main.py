from fastapi import FastAPI
import asyncio
import logging
from stock_scraping_service import stock_scraping_service
from dividend_scraping_service import dividend_scraping_service
from spreadsheet_update_service import spreadsheet_update_service
from market_update_service import market_update_service
from google.cloud import logging as cloud_logging
from fastapi.middleware.cors import CORSMiddleware

# Cloud Logging クライアントを初期化
client = cloud_logging.Client()
client.setup_logging()

# ロガーを取得
logger = logging.getLogger("uvicorn")

app = FastAPI()

# 許可するオリジン
origins = ["http://localhost:3000", "https://stock-scraping-webapp.vercel.app"]

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
        logger.info("stock_scraping: start")
        await stock_scraping_service.stock_scraping()
        logger.info("stock_scraping: done")

    if dividend:
        logger.info("dividend_scraping: start")
        await dividend_scraping_service.dividend_scraping()
        logger.info("dividend_scraping: done")

    if dividend or market:  # dividendを実行するとmarket情報が削除されるため
        logger.info("market_update_service: start")
        await market_update_service.update_market_and_industries()
        logger.info("market_update_service: done")

    if spreadsheet:
        logger.info("spreadsheet_update: start")
        await spreadsheet_update_service.spreadsheet_update()
        logger.info("spreadsheet_update: done")


@app.get("/update_stock_info")
async def update_stock_info(
    stock: bool = False,
    dividend: bool = False,
    market: bool = False,
    spreadsheet: bool = False,
):
    logger.info("リクエストを受け付けました")
    parameters = f"stock: {stock}, dividend: {dividend}, market: {market}, spreadsheet: {spreadsheet}"
    try:
        logger.info(parameters)
        asyncio.create_task(
            async_update_stock_info(stock, dividend, market, spreadsheet)
        )
        return {"message": parameters}
    except Exception as e:
        logger.error("error_message: ", exc_info=e)
        return {"message": "エラーです"}
