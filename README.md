🪙 CoinMarketCap Crypto Scraper

This project scrapes live cryptocurrency data from https://coinmarketcap.com using Selenium and BeautifulSoup, and exports the results to a CSV file.

🚀 Features
- Headless scraping using Selenium (Chrome)
- BeautifulSoup for parsing HTML tables
- Dynamic scrolling to load all coin data
- CSV export with timestamped filenames
- Follows Singleton & Page Object Pattern
- Clean, modular Python architecture

📁 Project Structure

CoinsMarket/
- ├── CsvFiles/                # Output CSV reports
- ├── req.txt                  # Project dependencies
- ├── run.bat / run.sh         # Easy command-line runner (Windows / Linux)
- ├── src/
- │   ├── Runner/
- │   │   └── main.py          # Main class entry point
- │   ├── pages/
- │   │   └── Home_AllCrypto_Page.py  # Page Object for CoinMarketCap
- │   ├── steps/
- │   │   └── ScrapeCoins.py   # Coin parsing logic
- │   └── utils/
- │       ├── commonActions.py # Utility wait + scroll actions
- │       └── CsvImp.py        # CSV writer

📦 Setup

1. Clone the repo
   git clone https://github.com/yourusername/CoinMarketCap-Scraper.git
   cd CoinMarketCap-Scraper

2. Install dependencies
   pip install -r req.txt

   Or use the run.bat script:
   run.bat

🧪 How to Run

   python -m src.Runner.main

This will:
- Launch a headless browser
- Scroll through all coins
- Extract data
- Save it in CsvFiles/crypto_<timestamp>.csv

🛠 Dependencies

- selenium
- beautifulsoup4
- webdriver-manager

Install them with:
   pip install -r req.txt

📌 Notes

- Make sure Chrome is installed (used by webdriver-manager)
- Adjust scroll behavior if CoinMarketCap changes its structure
