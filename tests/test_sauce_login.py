import pytest
from pages.sauce_login_page import LoginPage
from utils.webdriver_factory import create_chrome_driver

@pytest.fixture(scope="function")
def driver():
    _driver = create_chrome_driver()
    yield _driver
    _driver.quit()

def test_valid_login(driver):
    driver.get("https://www.saucedemo.com/")
    page = LoginPage(driver)    
    page.enter_username("standard_user")
    page.enter_password("secret_sauce")
    page.click_login()
    assert "inventory.html" in driver.current_url
