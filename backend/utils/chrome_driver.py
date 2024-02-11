from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def boot_driver():
    print("driverを起動します")

    # Chrome オプションの設定
    chrome_options = Options()
    chrome_options.add_argument(
        "--no-sandbox"
    )  # Chrome の保護機能を無効化する（Docker環境で動かすため）
    chrome_options.add_argument("--headless")  # ヘッドレスモードを有効にする
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_experimental_option(
        "prefs",
        {
            "download.default_directory": "/app/stock_scraping_service"  # Docker環境用のパス
        },
    )

    # Docker環境専用の記述
    chrome_driver_path = "/usr/local/bin/chromedriver"

    # ドライバーの起動
    driver = webdriver.Chrome(
        # ChromeDriverManager().install(), Docker環境で動かすときは不要
        options=chrome_options,
        executable_path=chrome_driver_path,
    )
    print("driverを起動しました")
    return driver
