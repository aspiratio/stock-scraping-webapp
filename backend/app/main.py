from fastapi import FastAPI

app = FastAPI()  # FastAPIのインスタンス化


# 基本（GET）
@app.get("/")  # インスタンス化したappにHTTPメソッド（オペレーションと呼ぶ）のGETで"/"のURLにアクセスがあったら下の関数を実行するという意味
async def root():
    return {"message": "Hello World"}
