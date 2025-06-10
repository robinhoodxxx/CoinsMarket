from bs4 import BeautifulSoup

from src.hooks.chromeDriver import ThreadSafeSingletonMeta
from src.pages.Home_AllCrypto_Page import Home_AllCrypto_Page


class ScrapeCoins_stepDef(metaclass=ThreadSafeSingletonMeta):
    default: str = "na"
    page = Home_AllCrypto_Page()

    def ScrappingAllCoins_step(self, driver) -> list[dict[str, str]]:
        print(f"current page:{driver.current_url}")
        self.page.sort_by_header_name(driver)
        self.page.gradual_scroll_down(driver)
        self.page.scroll_to_element(driver)
        # l = self.page.getLastPageIndex(driver)
        self.page.wait_for_full_table(driver)
        html = driver.page_source
        return self.Scraper(html)

    def Scraper(self, html) -> list[dict[str, str]]:
        doc = BeautifulSoup(html, "html.parser")
        body = doc.find('tbody')
        trs = body.contents
        print(len(trs))
        return self.Scrape_all_coins(trs)

    def Scrape_all_coins(self, trs) -> list[dict[str, str]]:
        def safe_get_text(elem) -> str:
            return elem.text.strip() if elem else self.default

        def is_coin_down(elem) -> str:
            if elem.find('span', class_="icon-Caret-down"):
                return "-"
            else:
                return ""

        coins_list = []

        for i, tr in enumerate(trs):
            try:
                tds = tr.find_all("td")
                if len(tds) < 11:
                    continue  # Skip if row is too short

                name_td = tds[2]
                price_td = tds[3]
                hr_1_td = tds[4]
                day_1_td = tds[5]
                day_7_td = tds[6]
                mcap_td = tds[7]
                vol_td = tds[8]
                supply_td = tds[9]
                last_7d_td = tds[10]

                coin_img = name_td.find("img", class_="coin-logo")
                coin_img_link = coin_img["src"] if coin_img else self.default

                coin_name_tag = name_td.find_all("p")
                coin_name = coin_name_tag[0].get_text(strip=True) if len(coin_name_tag) > 0 else self.default
                coin_symbol = coin_name_tag[1].get_text(strip=True) if len(coin_name_tag) > 1 else self.default

                coin_price = safe_get_text(price_td.find('span'))
                coin_1hr = is_coin_down(hr_1_td) + safe_get_text(hr_1_td.find('span'))
                coin_1day = is_coin_down(day_1_td) + safe_get_text(day_1_td.find('span'))
                coin_7day = is_coin_down(day_7_td) + safe_get_text(day_7_td.find('span'))

                coin_mcap = safe_get_text(mcap_td.find('span'))

                p_tags = vol_td.find_all('p')
                coin_vol_24h = p_tags[0].get_text(strip=True) if len(p_tags) > 0 else self.default
                coin_vol_24h_units = p_tags[1].get_text(strip=True) if len(p_tags) > 1 else self.default

                circ_supply = supply_td.find('div', class_="circulating-supply-value")
                coin_circ_supply = safe_get_text(circ_supply)

                graph_img = last_7d_td.find('img')
                coin_graph = graph_img['src'] if graph_img else self.default

                coins_list.append({
                    "Name": coin_name,
                    "Symbol": coin_symbol,
                    "Price($)": coin_price,
                    "Img": coin_img_link,
                    "1hr%": coin_1hr,
                    "24hr%": coin_1day,
                    "7d%": coin_7day,
                    "MarketCap($)": coin_mcap,
                    "Volume($)_24hr": coin_vol_24h,
                    "Volume_24hr": coin_vol_24h_units,
                    "CirculatingSupply": coin_circ_supply,
                    "Last7Days": coin_graph
                })
            except Exception as e:
                coins_list.append({"Name": f'Row:{i} got th exception {e}'})
                print(f"Error scraping row {i}: {e}")
                continue

        return coins_list
