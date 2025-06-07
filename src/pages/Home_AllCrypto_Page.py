import threading
import time
from src.utils.commonActions import commonActions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

class ThreadSafeSingletonMeta(type):
    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Home_AllCrypto_Page(commonActions,metaclass=ThreadSafeSingletonMeta):

    tableElements: str = "//table/tbody/tr"
    last_page: str = "(//ul[@class='pagination'])[last()]/li[@class='page'][last()]"



    def getLastPageIndex(self, driver) -> str:
        return self.waitFor(driver, self.last_page).text.strip()

    def waitTableElementsLoaded(self, driver) -> None:
        self.waitUntilPresenceAll(driver, self.tableElements)

    def wait_for_full_table(self,driver, expected_cols: int = 10,
                            timeout: int = 20):
        def table_fully_loaded(d):
            rows = d.find_elements(By.XPATH, self.tableElements)
            for row in rows:
                tds = row.find_elements(By.TAG_NAME, "td")
                if len(tds) < expected_cols:
                    return False
            return True

        WebDriverWait(driver, timeout).until(table_fully_loaded)

    def scroll_to_element(self,driver):
        element = driver.find_element(By.XPATH, self.last_page)
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)

    def gradual_scroll_down(self,driver, scroll_pause=0.2,scroll_step=1000, max_scrolls=50):
        """
        Gradually scroll down the page by small steps, to trigger lazy loading.

        :param driver: Selenium WebDriver
        :param scroll_pause: seconds to wait after each scroll
        :param scroll_step: pixels to scroll down each time
        :param max_scrolls: maximum number of scroll steps to avoid infinite loop
        """
        last_height = driver.execute_script("return window.pageYOffset")
        scrolls = 0

        while scrolls < max_scrolls:
            driver.execute_script(f"window.scrollBy(0, {scroll_step});")
            time.sleep(scroll_pause)

            new_height = driver.execute_script("return window.pageYOffset")
            if new_height == last_height:
                # No more scrolling possible (reached bottom)
                break
            last_height = new_height
            scrolls += 1

        print(f"Gradually scrolled down {scrolls} steps.")
