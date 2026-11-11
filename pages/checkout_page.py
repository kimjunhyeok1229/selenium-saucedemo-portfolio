from selenium.webdriver.common.by import By

from .base_page import BasePage


class CheckoutPage(BasePage):
    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    POSTAL_CODE = (By.ID, "postal-code")
    CONTINUE = (By.ID, "continue")
    FINISH = (By.ID, "finish")
    ERROR = (By.CSS_SELECTOR, "[data-test='error']")
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")

    def fill_info(self, first, last, postal):
        self.type(self.FIRST_NAME, first)
        self.type(self.LAST_NAME, last)
        self.type(self.POSTAL_CODE, postal)
        self.click(self.CONTINUE)

    def finish(self):
        self.click(self.FINISH)

    def error_message(self):
        return self.text_of(self.ERROR)

    def confirmation(self):
        return self.text_of(self.COMPLETE_HEADER)
