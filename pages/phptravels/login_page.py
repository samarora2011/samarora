import allure
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators.locators import LogInLocators, UserAccountLocators
from base.page_base import PageBase


class LogInPage(PageBase):
    def __init__(self, driver):
        super().__init__(driver)
        self.wait = WebDriverWait(driver, 20)

    @allure.step("Expanding account menu")
    def expand_account_menu(self):
        try:
            account_button = self.wait.until(EC.element_to_be_clickable(LogInLocators.account_menu_button))
            account_button.click()
        except Exception:
            # No account menu present yet or not needed; swallow and continue
            pass

    @allure.step("Opening login page")
    def open_login_page(self):
        login_button = self.wait.until(EC.element_to_be_clickable(LogInLocators.login_link))
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'}); arguments[0].click();",
            login_button
        )
        self.wait.until(EC.url_contains("/login"))

    @allure.step("Login with email: '{0}'")
    def set_user_inputs(self, email, password):
        self.wait.until(EC.element_to_be_clickable(LogInLocators.email_input)).send_keys(email)
        self.driver.find_element(*LogInLocators.password_input).send_keys(password)
        login_button = self.wait.until(EC.element_to_be_clickable(LogInLocators.login_button))
        login_button.click()

    @allure.step("Logout")
    def logout(self):
        logout_url = self.driver.base_url.rstrip('/') + '/logout'
        self.driver.get(logout_url)
        self.wait.until(EC.url_contains('/login'))
