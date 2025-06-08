import concurrent.futures
import math
import time
from datetime import datetime
from queue import Queue
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from src.steps.ScrapeCoins_stepDef import ScrapeCoins_stepDef
from src.utils.CsvImp import CsvWriter

TOTAL_PAGES = 10
CHUNK_SIZE = 5
THREADS = math.ceil(TOTAL_PAGES / CHUNK_SIZE)

result_queue = Queue()


def scrape_single_page(page_num):
    url = f"https://coinmarketcap.com/?page={page_num}"
    options = Options()
    options.add_argument("--headless=new")  # run headless for performance
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    print("launched headless chrome browser")
    driver.maximize_window()
    s = ScrapeCoins_stepDef()

    try:
        driver.get(url)
        # do scraping and return list of dicts
        coins = s.ScrappingAllCoins_step(driver)

        return coins
    finally:
        driver.quit()


def scrape_pages(start_page, end_page):
    all_coins = []

    for page_num in range(start_page, end_page + 1):
        try:
            coins = scrape_single_page(page_num)  # Your method to scrape one page
            all_coins.extend(coins)
        except Exception as e:
            print(f"Error scraping page {page_num}: {e}")
    return all_coins


def worker(page_range):
    start_page, end_page = page_range
    result = scrape_pages(start_page, end_page)
    result_queue.put(result)


def run_parallel_scraping():
    # Split pages into chunks
    page_ranges = [
        (i, min(i + CHUNK_SIZE - 1, TOTAL_PAGES))
        for i in range(1, TOTAL_PAGES + 1, CHUNK_SIZE)
    ]

    with concurrent.futures.ThreadPoolExecutor(max_workers=THREADS) as executor:
        executor.map(worker, page_ranges)

    # Merge all results
    final_data = []
    while not result_queue.empty():
        final_data.extend(result_queue.get())

    return final_data


# Main Execution
if __name__ == "__main__":
    start_time = time.time()
    now = datetime.now()
    formatted = now.strftime("%y-%m-%d-%H-%M-%S")
    data = run_parallel_scraping()
    CsvWriter("parallel"+formatted,data)
    end_time = time.time()
    total_time = end_time - start_time
    print(f"⏱️ Total execution time: {total_time:.2f} seconds")
