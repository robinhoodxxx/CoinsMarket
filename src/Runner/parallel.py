import concurrent.futures
import math
import sys
import time
import traceback
from datetime import datetime
from src.hooks.chromeDriver import chromeDriver
from src.steps.ScrapeCoins_stepDef import ScrapeCoins_stepDef
from src.utils.CsvImp import CsvWriter, get_page_range

THREADS = 4


def scrape_pages(page_range):
    url_base = "https://coinmarketcap.com/?page="
    start_page, end_page = page_range
    print(f"Launched headless Chrome browser for pages {start_page} to {end_page}")

    all_coins = []
    failed_pages = []

    ch = chromeDriver()
    s = ScrapeCoins_stepDef()
    driver = ch.get_chrome_driver()

    try:
        for page_num in range(start_page, end_page + 1):
            try:
                driver.get(f"{url_base}{page_num}")
                time.sleep(1)
                coins = s.ScrappingAllCoins_step(driver)
                all_coins.extend(coins)
            except Exception as e:
                print(f"Error scraping page {page_num}: {e}")
                traceback.print_exc()
                failed_pages.append(page_num)
                # Reset the driver and scraper for next attempt
                try:
                    ch.quit_driver()
                except:
                    pass
                ch = chromeDriver()
                s = ScrapeCoins_stepDef()
                driver = ch.get_chrome_driver()
    finally:
        ch.quit_driver()

    return all_coins, failed_pages



def run_parallel_scraping(first_page: int, last_page: int):
    CHUNK_SIZE = math.ceil((last_page - first_page + 1) / THREADS)
    page_ranges = [
        (i, min(i + CHUNK_SIZE - 1, last_page))
        for i in range(first_page, last_page + 1, CHUNK_SIZE)
    ]

    final_data = []
    all_failed_pages = []

    with concurrent.futures.ProcessPoolExecutor(max_workers=THREADS) as executor:
        results = executor.map(scrape_pages, page_ranges)
        for coins, failed in results:
            final_data.extend(coins)
            all_failed_pages.extend(failed)

    with open("failed_pages.log", "w") as f:
       if all_failed_pages:
          f.write(str(all_failed_pages))  # Writes like [1, 2, 3]
       else:
           f.write("No pages failed")

    # Retry failed pages one by one
    if all_failed_pages:
        print(f"\nRetrying failed pages: {all_failed_pages}\n")

        ch = chromeDriver()
        driver = ch.get_chrome_driver()
        s = ScrapeCoins_stepDef()

        for page_num in all_failed_pages:
            try:
                driver.get(f"https://coinmarketcap.com/?page={page_num}")
                time.sleep(1)  # Add delay before retry
                coins = s.ScrappingAllCoins_step(driver)
                final_data.extend(coins)
            except Exception as e:
                print(f"Retry failed for page {page_num}: {e}")
            finally:
                ch.quit_driver()

    return final_data


# Main Execution
if __name__ == "__main__":
    first_page, last_page = get_page_range()

    if first_page < 1 or last_page > 98:
        sys.exit(f"first_page must be between < 1 and last_page <= 98. You provided: first_page->{first_page}&last_page->{last_page}")
    elif last_page < first_page:
        sys.exit(f'last_page must be greater than first_page. You provided: first_page->{first_page}&last_page->{last_page}')

    start_time = time.time()
    print(f"Scrapping total pages :{last_page - first_page + 1}")
    coins_list = run_parallel_scraping(first_page, last_page)

    now = datetime.now()
    formatted = now.strftime("%y%m%d-%H%M%S")

    CsvWriter(f'parallel_{formatted}_{first_page}-{last_page}', coins_list)

    end_time = time.time()
    total_time = end_time - start_time
    print(f"Total execution time: {total_time:.2f} seconds")
