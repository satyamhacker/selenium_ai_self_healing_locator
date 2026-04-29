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
    
