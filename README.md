# stock-scraping-webapp

自身が保有している株と配当金情報を集計し、Web 上で確認できるアプリケーション

## 設計概要

- DB：Firestore
- フロント：Next.js
  - （できれば）スプレッドシートのグラフを画面に表示したい
  - （できれば）分類ごとの保有株情報を画面に表示したい
- バックエンド：以下の粒度でサービスを分けた CloudRun（HTTPS エンドポイントを利用する）
  - 保有株情報の更新
    - 証券会社のページをスクレイピングして保有株情報を取得
    - DB から前回取得した株情報を取得
    - 今回と前回の株情報を比較して、同じであればここで処理を終了する
      違いがあれば今回の株情報を DB に登録
  - 配当金情報の更新
    - DB に登録された保有株の企業コードを取得する
    - 対象の企業コードだけ株価情報サイトでスクレイピングして配当金情報を取得
    - 取得した配当金情報を DB に登録する
  - スプレッドシートの更新
    - DB に登録された株情報と配当金情報を元に、スプレッドシートを更新する

## 開発用のメモ

### 実行環境

- M1 Mac
- Docker Desktop の「Use Rosetta for x86/amd64 emulation on Apple Silicon」をオン

### ビルド

backend ディレクトリで下記コマンドを実行

```sh
docker compose build
```

### コンテナ起動

```sh
docker compose up -d
```

### コンテナ内のターミナルに接続

```sh
docker exec -it stock_scraping_api_container /bin/bash
```
