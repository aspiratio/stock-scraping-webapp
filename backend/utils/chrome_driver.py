from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from utils.logger import Logger

logger = Logger()


def boot_driver():
    # Chrome オプションの設定
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")  # Chrome の保護機能を無効化する（Docker環境で動かすため）
    chrome_options.add_argument("--headless")  # ヘッドレスモードを有効にする
    chrome_options.add_argument("--disable-gpu")  # GPUを無効にする
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Docker環境専用の記述
    chrome_driver_path = "/usr/local/bin/chromedriver"

    # ドライバーの起動
    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=chrome_options,
        executable_path=chrome_driver_path,
    )
    print("driverを起動しました")
    logger.info("driverを起動しました")
    return driver
