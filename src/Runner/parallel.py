import concurrent.futures
import math
import sys
import time
from datetime import datetime
from queue import Queue
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from src.steps.ScrapeCoins_stepDef import ScrapeCoins_stepDef
from src.utils.CsvImp import CsvWriter, get_page_range

CHUNK_SIZE = 9
result_queue = Queue()



def scrape_pages(start_page, end_page):
    url_base = "https://coinmarketcap.com/?page="
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    print(f"Launched headless Chrome browser for pages {start_page} to {end_page}")
    driver.maximize_window()
    s = ScrapeCoins_stepDef()

    all_coins = []
    try:
        for page_num in range(start_page, end_page + 1):
            try:
                driver.get(f"{url_base}{page_num}")
                coins = s.ScrappingAllCoins_step(driver)
                all_coins.extend(coins)
            except Exception as e:
                print(f"Error scraping page {page_num}: {e}")
    finally:
        driver.quit()

    return all_coins


def worker(page_range):
    start_page, end_page = page_range
    result = scrape_pages(start_page, end_page)
    result_queue.put(result)


def run_parallel_scraping(first_page: int, last_page: int):
    THREADS = math.ceil((last_page - first_page + 1) / CHUNK_SIZE)
    # Split pages into chunks
    page_ranges = [
        (i, min(i + CHUNK_SIZE - 1, last_page))
        for i in range(first_page, last_page + 1, CHUNK_SIZE)
    ]

    with concurrent.futures.ProcessPoolExecutor(max_workers=THREADS) as executor:
        executor.map(worker, page_ranges)

    # Merge all results
    final_data = []
    while not result_queue.empty():
        final_data.extend(result_queue.get())

    return final_data


# Main Execution
if __name__ == "__main__":

    first_page, last_page = get_page_range()

    if first_page < 1 or last_page > 98:
        sys.exit(
            f"first_page must be between < 1 and last_page <= 98. You provided: first_page->{first_page}&last_page->{last_page}")  # Or raise an error
    elif last_page < first_page:
        sys.exit(
            f'last_page must be greater than first_page. You provided: first_page->{first_page}&last_page->{last_page}')

    start_time = time.time()

    print(f"Scrapping total pages :{last_page - first_page + 1}")

    now = datetime.now()
    formatted = now.strftime("%y%m%d-%H%M%S")
    coins_list = run_parallel_scraping(first_page, last_page)
    CsvWriter(f'parallel_{formatted}_{first_page}-{last_page}', coins_list)
    end_time = time.time()
    total_time = end_time - start_time
    print(f"Total execution time: {total_time:.2f} seconds")
