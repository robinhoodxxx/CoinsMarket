from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from src.pages.Home_AllCrypto_Page import Home_AllCrypto_Page
from src.utils.CsvImp import *
from src.steps.ScrapeCoins import ScrapeCoins


class Runner:
    #url = "https://coinmarketcap.com"
    url = "https://coinmarketcap.com/?page=98"

    def Scraper(self, html) -> None:
        doc = BeautifulSoup(html, "html.parser")
        body = doc.find('tbody')
        trs = body.contents
        print(len(trs))
        coins = ScrapeCoins.ScrapeFirstTen(self, trs)

        CsvWriter("crypto", coins)



if __name__ == '__main__':

    CsvWriter("hell",[])

    driver = webdriver.Chrome()

    try:

        # Open the page
        r = Runner()
        page = Home_AllCrypto_Page()

        driver.get(r.url)
        driver.maximize_window()


        r.Scraper(html)
    finally:
        driver.quit()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
