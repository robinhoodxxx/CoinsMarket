
🪙 CoinMarketCap Crypto Scraper

This project scrapes live cryptocurrency data from CoinMarketCap (https://coinmarketcap.com) using Selenium, BeautifulSoup, and parallel processing. It exports the results into a CSV file, with support for retrying failed pages and logging errors.

🚀 Features

- ⚡ Parallel scraping with concurrent.futures
- 🧭 Retries failed pages with isolated browser sessions
- 🧠 Thread-safe Singleton design for Chrome driver & logic classes
- 🧼 Clean architecture using Page Object Model (POM)
- 🧾 CSV export with auto-named timestamped files
- 🗃 Logs failed pages to failed_pages.log

📁 Project Structure

CoinsMarket/
- ├── CsvFiles/                # Output CSV reports
- ├── failed_pages.log         # Logs failed pages during scrape
- ├── req.txt                  # Project dependencies
- ├── run.bat / run.sh         # Easy command-line runners
- ├── src/
- │   ├── Runner/
- │   │   └── parallel.py      # Entry point with parallel scraping
- │   ├── hooks/
- │   │   └── chromeDriver.py  # Chrome driver Singleton
- │   ├── pages/
- │   │   └── Home_AllCrypto_Page.py  # Page Object for CoinMarketCap
- │   ├── steps/
- │   │   └── ScrapeCoins_stepDef.py  # Parsing logic for coins
- │   └── utils/
- │       ├── CsvImp.py        # CSV writer and page range input
- │       └── commonActions.py # Scrolling, waits, utility actions

📦 Setup

- git clone https://github.com/robinhoodxxx/CoinsMarket.git
- cd CoinsMarket
- pip install -r req.txt

Run on Windows we have two bat files:
 1. run.bat (series run like scrape page one after one)
 2. runParallel.bat (parallel execution based on chuck size 
   i.e no of pages you wanna scrape at a single time eg: chunk size is 5 then total pages is 50 you launched 50/5 ->10 browser parallel and scrape 5 pages in each browser)


🧪 How to Run man classes in cmd
python -m src.Runner.main (series execution)
This will:
1. Launch headless Chrome only once
2. Scrape the specified range of pages
4. Save the data to CsvFiles/<timestamp>.csv



python -m src.Runner.parallel (parallel execution)

This will:
1. Launch headless Chrome sessions in parallel
2. Scrape the specified range of pages
3. Retry failed pages individually
4. Save the data to CsvFiles/parallel_<timestamp>.csv
5. Log failed pages to failed_pages.log (as [1, 2, 5])

⚙️ Configuration

Define the page range using a prompt or utility function in get_page_range(). CHUNK_SIZE controls how many pages are processed per thread.

🛠 Dependencies

- selenium
- beautifulsoup4
- webdriver-manager

Install via:
- pip install -r req.txt

📌 Notes

- Ensure Google Chrome is installed (used by webdriver-manager)
- --disable-gpu improves headless stability but is optional locally
- Script automatically retries invalid session errors
- Compatible with Jenkins CI (CSV/logs can be archived as build artifacts)
