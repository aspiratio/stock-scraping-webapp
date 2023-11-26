from fastapi import FastAPI

from stock_scraping_service import stock_scraping_service

app = FastAPI()  # FastAPIのインスタンス化


# 基本（GET）
@app.get("/")  # インスタンス化したappにHTTPメソッド（オペレーションと呼ぶ）のGETで"/"のURLにアクセスがあったら下の関数を実行するという意味
async def root():
    print("リクエストを受け付けました")
    try:
        stock_scraping_service.stock_scraping_service()
        return {"message": "実行中です"}
    except Exception as e:
        print("An error occurred:", str(e))
        return {"message": "エラーです"}
