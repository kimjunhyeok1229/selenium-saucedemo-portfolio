from selenium.webdriver.common.by import By

from .base_page import BasePage


class InventoryPage(BasePage):
    LIST = (By.CLASS_NAME, "inventory_list")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")

    @staticmethod
    def _slug(product_name):
        return product_name.lower().replace(" ", "-")

    def wait_until_loaded(self):
        self.wait_for_url("inventory")
        self.visible(self.LIST)
        return self

    def add_to_cart(self, product_name):
        self.click((By.ID, f"add-to-cart-{self._slug(product_name)}"))

    def remove_from_cart(self, product_name):
        self.click((By.ID, f"remove-{self._slug(product_name)}"))

    def cart_count(self):
        badges = self.driver.find_elements(*self.CART_BADGE)
        return int(badges[0].text) if badges else 0

    def open_cart(self):
        self.click(self.CART_LINK)
