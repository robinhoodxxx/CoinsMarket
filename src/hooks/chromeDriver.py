import threading
from selenium import webdriver
from selenium.webdriver.chrome.options import Options



class ThreadSafeSingletonMeta(type):
    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class chromeDriver:
    def __init__(self):
        self.driver = None

    def get_chrome_driver(self):
        if self.driver is None:
            options = Options()
            options.add_argument("--headless")  # Use headless mode
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--window-size=1920,1080")
            options.add_argument('--disable-3d-apis')
            options.add_argument('--disable-software-rasterizer')  # Prevents software fallback
            options.add_argument('--enable-unsafe-swiftshader')  # Use with caution, bypasses warnings
            options.add_argument('--log-level=3')    # Suppresses most console logging (ERROR level)
            options.add_argument('--ignore-certificate-errors')  # Ignores bad SSL certs

            self.driver = webdriver.Chrome(
                options=options
            )
        return self.driver

    def quit_driver(self):
        if self.driver:
            self.driver.quit()
            self.driver = None
