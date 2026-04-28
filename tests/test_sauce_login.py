# tests/test_sauce_login.py

import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
from pages.sauce_login_page import LoginPage
from utils.webdriver_factory import create_chrome_driver

@pytest.fixture
def driver():
    # Create a ChromeDriver that matches the locally installed Chrome version.
    driver = create_chrome_driver()
    driver.maximize_window()
    yield driver
    driver.quit()

def test_valid_login(driver):
    # Navigate to saucedemo.com
    driver.get("https://www.saucedemo.com/")

    # LoginPage object initialize
    login_page = LoginPage(driver)

    # Perform login actions
    login_page.enter_username("standard_user")
    login_page.enter_password("secret_sauce")
    login_page.click_login()

    # Assertion: URL change ya element check
    assert "inventory.html" in driver.current_url
