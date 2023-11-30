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
    print("リクエストを受け付けました")
    if stock or dividend:
        print("ドライバーを起動します")
        driver = boot_driver()

    try:
        if stock:
            await stock_scraping_service.stock_scraping(driver)
        if dividend:
            await dividend_scraping_service.dividend_scraping(driver)
        if spreadsheet:
            await spreadsheet_update_service.spreadsheet_update()
        return {"message": "保有株情報を更新中です"}
    except Exception as e:
        return {"message": "エラーです"}
    finally:
        if stock or dividend:
            driver.quit()
