from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import logging
from google.cloud import logging as cloud_logging

# Cloud Logging クライアントを初期化
client = cloud_logging.Client()
client.setup_logging()

# ロガーを取得
logger = logging.getLogger("uvicorn")


# Docker環境用
def boot_driver(download_directory=""):
    logger.info("driverを起動します")

    # Chrome オプションの設定
    chrome_options = Options()
    chrome_options.add_argument(
        "--no-sandbox"
    )  # Chrome の保護機能を無効化する（Docker環境で動かすため）
    chrome_options.add_argument("--headless")  # ヘッドレスモードを有効にする
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")
    if download_directory:
        chrome_options.add_experimental_option(
            "prefs",
            {"download.default_directory": download_directory},
        )

    # Docker環境専用の記述
    chrome_driver_path = "/usr/local/bin/chromedriver"

    # ドライバーの起動
    driver = webdriver.Chrome(
        options=chrome_options,
        executable_path=chrome_driver_path,
    )
    logger.info("driverを起動しました")
    return driver


# venv環境用
def boot_driver_venv(download_directory=""):
    logger.info("driverを起動します")

    # Chrome オプションの設定
    chrome_options = Options()
    if download_directory:
        chrome_options.add_experimental_option(
            "prefs",
            {"download.default_directory": download_directory},
        )

    # ドライバーの起動
    driver = webdriver.Chrome(
        ChromeDriverManager().install(),
        options=chrome_options,
    )
    logger.info("driverを起動しました")
    return driver
