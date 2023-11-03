# ルートディレクトリでビルドコマンドを実行する
FROM python:3.11-slim

# aptパッケージマネージャが対話的なモードを使用しないように設定する
ENV DEBIAN_FRONTEND noninteractive

# Pythonで上階層を参照できるように親ディレクトリを環境変数に設定する
ENV PYTHONPATH "/app/:$PYTHONPATH"

# タイムゾーンをAsia/Tokyoにする
RUN cp -a /etc/localtime /etc/localtime.origin && ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime

# 必要なパッケージのインストール
RUN apt update
RUN apt install -y curl wget unzip

# Google Chromeをインストール
RUN wget -q --no-check-certificate https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
  && apt update && apt install -y ./google-chrome-stable_current_amd64.deb

# Chrome Driverをインストール
RUN CHROMEDRIVER_VERSION=$(curl -sS https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_STABLE) \
  && echo "Chrome Driver Version: $CHROMEDRIVER_VERSION" \
  && curl -sS -o /tmp/chromedriver_linux64.zip https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip \
  && echo "Downloaded Chrome Driver ZIP" \
  && ls -al /tmp \
  && unzip -d /usr/local/bin/ /tmp/chromedriver_linux64.zip \
  && echo "Unzipped Chrome Driver to /usr/local/bin/" \
  && ls -al /usr/local/bin/


WORKDIR /app/stock_scraping_service

# 必要なファイルを作業ディレクトリにコピー
COPY backend/stock_scraping_service/main.py .
COPY backend/stock_scraping_service/requirements.txt .
COPY backend/utils /app/utils

RUN pip install -r requirements.txt

CMD ["python", "main.py"]