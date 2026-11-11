import pytest

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

BACKPACK = "Sauce Labs Backpack"
BIKE_LIGHT = "Sauce Labs Bike Light"


@pytest.fixture
def inventory(driver):
    """Start every test already logged in on the inventory page."""
    LoginPage(driver).open().login("standard_user", "secret_sauce")
    return InventoryPage(driver).wait_until_loaded()


def test_add_item_updates_cart_badge(inventory):
    """TC-CART-001"""
    inventory.add_to_cart(BACKPACK)
    assert inventory.cart_count() == 1


def test_add_two_items_then_remove_one(inventory):
    """TC-CART-002"""
    inventory.add_to_cart(BACKPACK)
    inventory.add_to_cart(BIKE_LIGHT)
    assert inventory.cart_count() == 2

    inventory.remove_from_cart(BACKPACK)
    assert inventory.cart_count() == 1


def test_cart_page_lists_added_item(driver, inventory):
    """TC-CART-003"""
    inventory.add_to_cart(BACKPACK)
    inventory.open_cart()

    assert CartPage(driver).item_names() == [BACKPACK]


def test_checkout_happy_path(driver, inventory):
    """TC-CHECKOUT-001"""
    inventory.add_to_cart(BACKPACK)
    inventory.open_cart()
    CartPage(driver).checkout()

    checkout = CheckoutPage(driver)
    checkout.fill_info("Test", "User", "12345")
    checkout.finish()

    assert checkout.confirmation() == "Thank you for your order!"


def test_checkout_requires_first_name(driver, inventory):
    """TC-CHECKOUT-002"""
    inventory.add_to_cart(BACKPACK)
    inventory.open_cart()
    CartPage(driver).checkout()

    checkout = CheckoutPage(driver)
    checkout.fill_info("", "User", "12345")

    assert "First Name is required" in checkout.error_message()
