from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class commonActions:
    def waitFor(self, driver, locator: str, timeout: int = 10) -> WebElement:
        return (WebDriverWait(driver, timeout)
                .until(EC.visibility_of_element_located((By.XPATH, locator))
                       ))

    def waitUntilPresenceAll(self, driver, locator: str, timeout: int = 10) -> None:
        (WebDriverWait(driver, timeout)
        .until(
            EC.presence_of_all_elements_located((By.XPATH, locator))
        ))

    def waitUntilAll(self, driver, locator: str, timeout: int = 10) -> None:
        (WebDriverWait(driver, timeout)
        .until(
            EC.visibility_of_all_elements_located((By.XPATH, locator))
        ))

    def waitForAll(self, driver, locator: str, timeout: int = 10) -> list[WebElement]:
        return (WebDriverWait(driver, timeout)
        .until(
            EC.visibility_of_all_elements_located((By.XPATH, locator))
        ))



