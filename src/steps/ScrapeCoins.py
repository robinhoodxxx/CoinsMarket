
from bs4 import  BeautifulSoup
from src.pages.Home_AllCrypto_Page import Home_AllCrypto_Page
from src.utils.CsvImp import CsvWriter


class ScrapeCoins:
    default :str ="na"
    page = Home_AllCrypto_Page()



    def ScrappingAllCoins_step(self,driver):
        self.page.gradual_scroll_down(driver)
        self.page.scroll_to_element(driver)
        l = self.page.getLastPageIndex(driver)
        print(f'{l}->pages')
        self.page.wait_for_full_table(driver)
        html = driver.page_source
        self.Scraper(html)


    def Scraper(self, html) -> None:
        doc = BeautifulSoup(html, "html.parser")
        body = doc.find('tbody')
        trs = body.contents
        print(len(trs))
        coins = ScrapeCoins.ScrapeFirstTen(self, trs)

        CsvWriter("crypto", coins)

    def ScrapeRemaingcoins(self, trs) -> list[dict]:
        remaing_coins = []
        for i in range(10, len(trs)):
            tds = trs[i].contents

            name = tds[2].a.find_all("p")
            price = tds[3]
            coin_name = name[1].text
            coin_symbol = name[2].text
            coin_price = price.span.text

            coin = {
                "Name": coin_name,
                "Symbol": coin_symbol,
                "Price": coin_price
            }
            remaing_coins.append(coin)
            # print(coin)

        return remaing_coins

    def ScrapeFirstTen(self,trs) :
        coins_list = []
        for i in range(len(trs)):
            tds = trs[i].contents
            print(i)
            name = tds[2]
            price = tds[3]
            hr_1 = tds[4]
            day_1 = tds[5]
            day_7 = tds[6]
            m_cap = tds[7]
            vol_24hr = tds[8]
            c_sup = tds[9]
            lst_7d = tds[10]

            coinImgLink = name.find("img", class_="coin-logo")["src"]
            coin = name.find_all('p')
            coinName = coin[0].get_text(strip=True) if coin else self.default
            coinSymbol = coin[1].get_text(strip=True) if coin else self.default

            coinPrice = price.find('span').text

            coin_1hr = hr_1.find('span').text

            coin_1day = day_1.find('span').text

            coin_7day = day_7.find('span').text

            coin_market_cap = m_cap.find('span').text if m_cap.find('span') else self.default

            p_tags = vol_24hr.find_all('p')
            coin_volume_24hr = p_tags[0].get_text(strip=True) if p_tags else self.default
            coin_volume_24hr_in_coins = p_tags[1].get_text(strip=True) if p_tags else self.default

            coin_circulating_supply_is_available = c_sup.find('div', class_="circulating-supply-value")
            coin_circulating_supply = coin_circulating_supply_is_available.span.text if coin_circulating_supply_is_available else self.default

            coin_last_7d = lst_7d.find('img')['src']

            coin = {
                'Name': coinName,
                "Symbol": coinSymbol,
                "Price": coinPrice,
                "Img": coinImgLink,
                "1hr%": coin_1hr,
                "24hr%": coin_1day,
                "7d%": coin_7day,
                "MarketCap": coin_market_cap,
                "Volume(24h)": coin_volume_24hr,
                "Vol(24h)": coin_volume_24hr_in_coins,
                "CirculatingSupply": coin_circulating_supply,
                "Last7Days": coin_last_7d
            }

            coins_list.append(coin)

        return coins_list
