import pytest

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

PASSWORD = "secret_sauce"


@pytest.fixture
def login_page(driver):
    return LoginPage(driver).open()


def test_login_success(driver, login_page):
    """TC-LOGIN-001"""
    login_page.login("standard_user", PASSWORD)
    InventoryPage(driver).wait_until_loaded()


@pytest.mark.parametrize(
    "username, password, expected",
    [
        ("standard_user", "wrong_password", "Username and password do not match"),
        ("locked_out_user", PASSWORD, "locked out"),
        ("", PASSWORD, "Username is required"),
        ("standard_user", "", "Password is required"),
    ],
    ids=["wrong-password", "locked-out", "empty-username", "empty-password"],
)
def test_login_errors(driver, login_page, username, password, expected):
    """TC-LOGIN-002 ~ 005"""
    login_page.login(username, password)

    assert expected in login_page.error_message()
    assert "inventory" not in driver.current_url


@pytest.mark.parametrize(
    "username", ["standard_user", "problem_user", "performance_glitch_user"]
)
def test_login_allowed_users(driver, login_page, username):
    """TC-LOGIN-006"""
    login_page.login(username, PASSWORD)
    InventoryPage(driver).wait_until_loaded()
