import threading
import time

from selenium.common import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.chrome.webdriver import WebDriver

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


class Home_AllCrypto_Page(commonActions, metaclass=ThreadSafeSingletonMeta):
    tableElements: str = "//table/tbody/tr"
    last_page: str = "(//ul[@class='pagination'])[last()]/li[@class='page'][last()]"
    name_header: str = "//table/thead/tr/th//p[text()='Name']"

    def getLastPageIndex(self, driver) -> str:
        return self.waitFor(driver, self.last_page).text.strip()

    def sort_by_header_name(self, driver):
        self.waitClick(driver, self.name_header).click()

    def waitTableElementsLoaded(self, driver) -> None:
        self.waitUntilPresenceAll(driver, self.tableElements)

    def wait_for_full_table(self, driver, expected_cols: int = 10,
                            timeout: int = 20):
        def table_fully_loaded(d):
            rows = d.find_elements(By.XPATH, self.tableElements)
            for row in rows:
                tds = row.find_elements(By.TAG_NAME, "td")
                if len(tds) < expected_cols:
                    return False
            return True

        WebDriverWait(driver, timeout).until(table_fully_loaded)

    def gradual_scroll_down(self, driver, scroll_pause=0.5, scroll_step=800, max_scrolls=50):
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

    def scroll_to_element(self, driver: WebDriver, selector: str = last_page, by: str = By.XPATH, center: bool = True,
                          pause: float = 0.2) -> None:
        """
        Scrolls to the given element using scrollIntoView.

        :param driver: Selenium WebDriver
        :param selector: Element locator (XPath or CSS)
        :param by: Locator strategy ('xpath' or 'css selector')
        :param center: If True, scrolls element to center of viewport. Else to top.
        :param pause: Time to pause after scroll
        """
        try:
            element = driver.find_element(by, selector)
            driver.execute_script(
                "arguments[0].scrollIntoView({ behavior: 'smooth', block: arguments[1] });",
                element,
                'center' if center else 'start'
            )
            time.sleep(pause)
            # return element  # Optional: return it for further actions
        except (NoSuchElementException, StaleElementReferenceException) as e:
            print(f"scroll_to_element failed: {e}")
            return None
