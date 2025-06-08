import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from src.steps.ScrapeCoins_stepDef import ScrapeCoins_stepDef
from src.utils.CsvImp import CsvWriter


if __name__ == '__main__':

    start_time = time.time()

    now = datetime.now()
    formatted = now.strftime("%y-%m-%d-%H-%M-%S")
    options = Options()
    options.add_argument("--headless")  # run headless for performance
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome()
    print("launched headless chrome browser")
    driver.maximize_window()

    s = ScrapeCoins_stepDef()
    coins_list = []
    try:
        for i in range(1,5):
            url = f'https://coinmarketcap.com/?page={i}'
            print(f'Navigated to page: {url}')
            driver.get(url)
            coins_list.extend(s.ScrappingAllCoins_step(driver))

        CsvWriter(formatted,coins_list)


    finally:
        driver.quit()


    end_time = time.time()
    total_time = end_time - start_time
    print(f"⏱️ Total execution time: {total_time:.2f} seconds")
