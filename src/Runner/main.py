import sys
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from src.hooks.chromeDriver import chromeDriver
from src.steps.ScrapeCoins_stepDef import ScrapeCoins_stepDef
from src.utils.CsvImp import CsvWriter, get_page_range

if __name__ == '__main__':

    first_page, last_page = get_page_range()

    if first_page < 1 or last_page > 98:
        sys.exit(
            f"first_page must be between < 1 and last_page <= 98. You provided: first_page->{first_page}&last_page->{last_page}")  # Or raise an error
    elif  last_page < first_page:
        sys.exit(f'last_page must be greater than first_page. You provided: first_page->{first_page}&last_page->{last_page}')

    start_time = time.time()

    print(f"Scrapping total pages :{last_page - first_page + 1}")

    ch =chromeDriver()
    now = datetime.now()
    formatted = now.strftime("%y%m%d-%H%M%S")
    driver = ch.get_chrome_driver()
    print("launched headless chrome browser")
    driver.maximize_window()

    s = ScrapeCoins_stepDef()
    coins_list = []
    try:
        for i in range(first_page, last_page + 1):
            url = f'https://coinmarketcap.com/?page={i}'
            driver.get(url)
            coins_list.extend(s.ScrappingAllCoins_step(driver))

        CsvWriter(f'{formatted}_{last_page}', coins_list)


    finally:
        ch.quit_driver()

    end_time = time.time()
    total_time = end_time - start_time
    print(f"Total execution time: {total_time:.2f} seconds")
