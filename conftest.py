import os
import re
from datetime import datetime
from pathlib import Path

import pytest
from selenium import webdriver

try:  # optional: only needed when running with --html
    from pytest_html import extras as html_extras
except ImportError:  # pragma: no cover
    html_extras = None

SCREENSHOT_DIR = Path(__file__).parent / "screenshots"


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """On a failed test body, save a screenshot and embed it in the HTML report.

    This runs while the browser is still open (fixture teardown comes later).
    """
    outcome = yield
    report = outcome.get_result()

    if report.when != "call" or not report.failed:
        return
    drv = item.funcargs.get("driver") or item.funcargs.get("logged_in_driver")
    if drv is None:
        return

    SCREENSHOT_DIR.mkdir(exist_ok=True)
    safe_name = re.sub(r"[^\w\-]+", "_", item.name)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = SCREENSHOT_DIR / f"{safe_name}_{stamp}.png"
    drv.save_screenshot(str(path))
    print(f"\n[screenshot saved] {path}")

    if html_extras is not None:
        extra = getattr(report, "extras", [])
        extra.append(html_extras.png(drv.get_screenshot_as_base64(), "Failure screenshot"))
        extra.append(html_extras.url(drv.current_url, "Page URL at failure"))
        report.extras = extra


@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    # Disable Chrome's password manager / leak-detection popups,
    # which can cover the page and break clicks during login tests.
    options.add_experimental_option(
        "prefs",
        {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.password_manager_leak_detection": False,
        },
    )
    # HEADLESS=1 runs without a visible window (needed later for CI).
    if os.getenv("HEADLESS") == "1":
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        # Needed on Linux CI runners (limited /dev/shm, no user sandbox).
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

    drv = webdriver.Chrome(options=options)
    if os.getenv("HEADLESS") != "1":
        drv.maximize_window()

    yield drv  # the test runs here

    drv.quit()  # always closes the browser, even if the test fails
