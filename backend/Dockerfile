# ルートディレクトリでビルドコマンドを実行する
FROM python:3.11-slim

# aptパッケージマネージャが対話的なモードを使用しないように設定する
ENV DEBIAN_FRONTEND noninteractive

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
  && curl -sS -o /tmp/chromedriver_linux64.zip https://storage.googleapis.com/chrome-for-testing-public/$CHROMEDRIVER_VERSION/linux64/chromedriver-linux64.zip \
  && unzip -d /tmp/ /tmp/chromedriver_linux64.zip \
  && mv /tmp/chromedriver-linux64/chromedriver /usr/local/bin/ \
  && rm -rf /tmp/chromedriver_linux64.zip /tmp/chromedriver-linux64

ENV PYTHONPATH=/app

COPY ./ /app/

WORKDIR /app

RUN pip install -r requirements.txt

RUN chmod +x start.sh
ENTRYPOINT ["/app/start.sh"]