import allure
from allure_commons.types import AttachmentType
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from locators.locators import SearchHotelsFormLocators, SearchTabsLocators


class SearchHotelsForm:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def _find_visible(self, locator):
        elements = self.driver.find_elements(*locator)
        for element in elements:
            if element.is_displayed():
                return element
        raise Exception(f"Visible element not found for locator {locator}")

    def _click_element(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        try:
            element.click()
        except StaleElementReferenceException:
            try:
                self.driver.execute_script("arguments[0].click();", element)
            except Exception:
                raise

    @allure.step("Opening phptravels.net website")
    def open_page(self):
        self.driver.get("https://phptravels.net")

        try:
            self.wait.until(EC.visibility_of_element_located(SearchHotelsFormLocators.destination_input))
        except TimeoutException:
            hotels_tab = self.wait.until(EC.element_to_be_clickable(SearchTabsLocators.hotels_tab))
            hotels_tab.click()
            self.wait.until(EC.visibility_of_element_located(SearchHotelsFormLocators.destination_input))

    @allure.step("Setting destination to '{destination}'")
    def set_destination(self, destination):
        element = self.wait.until(EC.visibility_of_element_located(SearchHotelsFormLocators.destination_input))
        element.clear()
        element.send_keys(destination)

        suggestion_items_xpath = (
            "//div[contains(@class,'p-2.5') and contains(@class,'cursor-pointer') "
            "and contains(@class,'border-b') and contains(@class,'transition-colors')]"
        )

        try:
            self.wait.until(EC.visibility_of_any_elements_located((By.XPATH, suggestion_items_xpath)))
            suggestions = [s for s in self.driver.find_elements(By.XPATH, suggestion_items_xpath) if s.is_displayed()]
            if suggestions:
                target = next((s for s in suggestions if destination.lower() in s.text.lower()), suggestions[0])
                self._click_element(target)
                return
        except TimeoutException:
            pass

        element.send_keys(Keys.ENTER)

    @allure.step("Setting date range from '{check_in}' to '{check_out}'")
    def set_date_range(self, check_in, check_out):
        # Set check-in date using JavaScript
        checkin_element = self.wait.until(EC.visibility_of_element_located(SearchHotelsFormLocators.checkin_input))
        self.driver.execute_script("arguments[0].value = arguments[1];", checkin_element, check_in)

        # Set check-out date using JavaScript
        checkout_element = self.wait.until(EC.visibility_of_element_located(SearchHotelsFormLocators.checkout_input))
        self.driver.execute_script("arguments[0].value = arguments[1];", checkout_element, check_out)

    def _open_guest_dropdown(self):
        dropdown_trigger = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//div[contains(@class,'input-dropdown') and .//span[contains(normalize-space(),'Guests')]]//div[contains(@class,'input cursor-pointer')]")
        ))
        open_dropdowns = self.driver.find_elements(By.XPATH,
            "//div[contains(@class,'input-dropdown') and .//span[contains(normalize-space(),'Guests')]]//div[contains(@class,'input-dropdown-content') and contains(@class,'show')]")
        if not open_dropdowns:
            dropdown_trigger.click()
            self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.input-dropdown-content.show')))

    def _set_guest_count(self, label, target_count):
        section_xpath = (
            f"//div[contains(@class,'input-dropdown-content show')]"
            f"//div[contains(@class,'flex items-center justify-between px-3 py-2 border-b border-gray-100')][.//div[contains(@class,'text-xs font-bold') and normalize-space()='{label}']]"
        )
        count_element = self.wait.until(
            lambda d: d.find_element(By.XPATH, section_xpath + "//span[contains(@class,'text-center') and normalize-space()!='']")
        )
        current_count = int(count_element.text.strip())
        clicks_needed = target_count - current_count

        if clicks_needed == 0:
            return

        if clicks_needed > 0:
            button = self.driver.find_element(By.XPATH, section_xpath + "//button[.//span[normalize-space()='add']]")
        else:
            button = self.driver.find_element(By.XPATH, section_xpath + "//button[.//span[normalize-space()='remove']]")
            clicks_needed = abs(clicks_needed)

        for _ in range(clicks_needed):
            button.click()

    @allure.step("Setting number of adults to '{adults_num}'")
    def set_adults_number(self, adults_num):
        self._open_guest_dropdown()
        self._set_guest_count('Adults', int(adults_num))

    @allure.step("Setting number of children to '{kids_num}'")
    def set_kids_number(self, kids_num):
        self._open_guest_dropdown()
        self._set_guest_count('Children', int(kids_num))

    @allure.step("Setting nationality to '{nationality}'")
    def set_nationality(self, nationality):
        nationality_trigger = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//div[contains(@class,'input-dropdown') and .//span[normalize-space()='Select Nationality']]//div[contains(@class,'input cursor-pointer')]")
        ))
        nationality_trigger.click()
        nationality_input = self.wait.until(lambda d: self._find_visible(SearchHotelsFormLocators.nationality_select))
        nationality_input.clear()
        nationality_input.send_keys(nationality)

        try:
            suggestion = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, f"//div[contains(@class,'input-dropdown-content') and .//input[@placeholder='Search country...']]//div[contains(@class,'input-dropdown-item') and contains(normalize-space(.), '{nationality}')][1]")
            ))
            suggestion.click()
        except Exception:
            nationality_input.send_keys(Keys.ENTER)

    @allure.step("Performing search")
    def search_perform(self):
        element = self.wait.until(lambda d: self._find_visible(SearchHotelsFormLocators.search_btn))
        element.click()
        self.wait.until(lambda d: "/stays/" in d.current_url)
        allure.attach(self.driver.get_screenshot_as_png(), name="search_results", attachment_type=AttachmentType.PNG)
