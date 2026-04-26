import pytest
import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators.locators import UserAccountLocators, LogInLocators
from pages.phptravels.login_page import LogInPage


@pytest.mark.usefixtures("setup")
class TestLogIn:

    @allure.title("Login with valid data test")
    @allure.description("This is test of login with valid data")
    def test_login_passed(self):
        log_in_page = LogInPage(self.driver)
        log_in_page.open()
        log_in_page.expand_account_menu()
        log_in_page.open_login_page()
        log_in_page.set_user_inputs("user@phptravels.com", "demouser")
        # Wait for dashboard page
        WebDriverWait(self.driver, 20).until(EC.url_contains("dashboard"))
        # Wait for welcome message
        WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located(UserAccountLocators.welcome_msg))
        welcome_msg = "Demo User"
        assert welcome_msg == self.driver.find_element(
            *UserAccountLocators.welcome_msg).get_attribute("innerText").strip()
        log_in_page.logout()

    @allure.title("Login with invalid email test")
    @allure.description("This is test of login with invalid email")
    def test_login_failed(self):
        log_in_page = LogInPage(self.driver)
        log_in_page.open()
        log_in_page.expand_account_menu()
        log_in_page.open_login_page()
        log_in_page.set_user_inputs("admin@phptravels.com", "demouser")
        error_msg = "Invalid Credentials"
        WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located(LogInLocators.invalid_data_msg)
        )
        assert error_msg in self.driver.find_element(
            *LogInLocators.invalid_data_msg).text
