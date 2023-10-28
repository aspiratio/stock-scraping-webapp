FROM python:3.11

# aptパッケージマネージャが対話的なモードを使用しないように設定する
ENV DEBIAN_FRONTEND noninteractive

# タイムゾーンをAsia/Tokyoにする
RUN cp -a /etc/localtime /etc/localtime.origin && ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime

# 必要なパッケージのインストール
RUN apt update
RUN apt install -y curl
RUN apt install -y wget
RUN apt install -y unzip
RUN apt install -y gpg

# Google Chromeをインストール
RUN wget -q --no-check-certificate https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
  && apt update && apt install -y ./google-chrome-stable_current_amd64.deb

# Chrome Driverをインストール
RUN CHROMEDRIVER_VERSION=`curl -sS https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_STABLE` \
  && curl -sS -o /tmp/chromedriver_linux64.zip https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/$CHROMEDRIVER_VERSION/linux64/chromedriver-linux64.zip \
	&& unzip -d /usr/local/bin/ /tmp/chromedriver_linux64.zip

WORKDIR /app

# 必要なファイルを作業ディレクトリにコピー
COPY stock_scraping_service/main.py .
COPY stock_scraping_service/firestore_utils.py .
COPY stock_scraping_service/config.py .
COPY stock_scraping_service/requirements.txt .
COPY sa.json .
COPY .env .

RUN pip install -r requirements.txt

CMD ["python", "main.py"]