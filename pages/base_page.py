from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    """Common helpers. Every wait lives here so tests never call sleep()."""

    URL = "https://www.saucedemo.com"

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout

    def _wait(self, timeout=None):
        return WebDriverWait(self.driver, timeout or self.timeout)

    def visible(self, locator, timeout=None):
        return self._wait(timeout).until(EC.visibility_of_element_located(locator))

    def click(self, locator):
        self._wait().until(EC.element_to_be_clickable(locator)).click()

    def type(self, locator, text):
        element = self.visible(locator)
        element.clear()
        element.send_keys(text)

    def text_of(self, locator):
        return self.visible(locator).text

    def wait_for_url(self, fragment, timeout=None):
        self._wait(timeout).until(EC.url_contains(fragment))
