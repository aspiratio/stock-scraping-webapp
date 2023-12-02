from fastapi import FastAPI

from stock_scraping_service import stock_scraping_service
from dividend_scraping_service import dividend_scraping_service
from spreadsheet_update_service import spreadsheet_update_service
from utils.chrome_driver import boot_driver

app = FastAPI()  # FastAPIのインスタンス化


# 基本（GET）
@app.get(
    "/update_stock_info"
)  # インスタンス化したappにHTTPメソッド（オペレーションと呼ぶ）のGETで"/"のURLにアクセスがあったら下の関数を実行するという意味
async def update_stock_info(
    stock: bool = True, dividend: bool = True, spreadsheet: bool = True
):
    try:
        if stock:
            print("stock_scraping: start")
            await stock_scraping_service.stock_scraping(driver)
            print("stock_scraping: done")
        if dividend:
            print("dividend_scraping: start")
            await dividend_scraping_service.dividend_scraping(driver)
            print("dividend_scraping: done")
        if spreadsheet:
            print("spreadsheet_update: start")
            await spreadsheet_update_service.spreadsheet_update()
            print("spreadsheet_update: done")
        return {"message": "保有株情報を更新中です"}
    except Exception as e:
        print("error_message: ", e)
        return {"message": "エラーです"}
