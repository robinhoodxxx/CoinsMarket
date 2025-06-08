import sys
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from src.steps.ScrapeCoins_stepDef import ScrapeCoins_stepDef
from src.utils.CsvImp import CsvWriter, get_page_range

if __name__ == '__main__':
    
    first_page,last_page = get_page_range()

    if not 1 <= last_page <= 98:
        sys.exit(f"last_page must be between 1 and 98. You provided: {last_page}")  # Or raise an error

    start_time = time.time()

    print(f"Scrapping total pages :{last_page}")

    now = datetime.now()
    formatted = now.strftime("%y%m%d-%H%M%S")
    options = Options()
    options.add_argument("--headless")  # run headless for performance
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
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
        driver.quit()

    end_time = time.time()
    total_time = end_time - start_time
    print(f"Total execution time: {total_time:.2f} seconds")
