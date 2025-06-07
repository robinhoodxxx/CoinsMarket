from datetime import datetime
from selenium import webdriver
from src.steps.ScrapeCoins import ScrapeCoins

if __name__ == '__main__':

    url = "https://coinmarketcap.com/?page=10"
    now = datetime.now()
    formatted = now.strftime("%y-%m-%d-%H-%M-%S")
    driver = webdriver.Chrome()
    s = ScrapeCoins()
    try:
        driver.get(url)
        driver.maximize_window()
        s.ScrappingAllCoins_step(driver, formatted)
    finally:
        driver.quit()

