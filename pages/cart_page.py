from selenium.webdriver.common.by import By

from .base_page import BasePage


class CartPage(BasePage):
    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    CHECKOUT_BUTTON = (By.ID, "checkout")

    def item_names(self):
        self.wait_for_url("cart")
        self.visible(self.ITEM_NAME)
        # Re-query inside the wait so a re-render cannot cause a stale element.
        return self._wait().until(
            lambda d: [e.text for e in d.find_elements(*self.ITEM_NAME)] or False
        )

    def checkout(self):
        self.click(self.CHECKOUT_BUTTON)
