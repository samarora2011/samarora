import allure
from allure_commons.types import AttachmentType
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators.locators import SearchToursFormLocators
from utils.functions import set_travellers_number


class SearchToursForm:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    @allure.step("Opening phptravels.net website")
    def open_page(self):
        self.driver.get("https://phptravels.net/tours")

    @allure.step("Setting tour destination: '{1}'")
    def set_tour_destination(self, tour_destination):
        destination_input = self.wait.until(EC.visibility_of_element_located(
            SearchToursFormLocators.destination_input
        ))
        destination_input.clear()
        destination_input.send_keys(tour_destination)

        try:
            suggestion = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, f"//div[contains(@class,'input-dropdown-item') and normalize-space(.)='{tour_destination}']")
            ))
            suggestion.click()
        except Exception:
            destination_input.send_keys(Keys.ENTER)

    @allure.step("Setting tour type: '{1}'")
    def set_tour_type(self, tour_type):
        dropdown = self.wait.until(EC.element_to_be_clickable(
            SearchToursFormLocators.tour_type_dropdown
        ))
        dropdown.click()
        option = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, f"//div[contains(@class,'input-dropdown-item') and normalize-space(.)='{tour_type}']")
        ))
        option.click()

    @allure.step("Setting tour date to '{1}'/'{2}'/'{3}'")
    def set_date(self, start_year, start_month, start_day):
        month_map = {
            'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06',
            'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12',
            'January': '01', 'February': '02', 'March': '03', 'April': '04', 'June': '06',
            'July': '07', 'August': '08', 'September': '09', 'October': '10', 'November': '11', 'December': '12'
        }
        month_key = start_month[:3] if len(start_month) >= 3 else start_month
        month_value = month_map.get(month_key, start_month)
        date_value = f"{int(start_day):02d}-{month_value}-{start_year}"

        date_input = self.wait.until(EC.visibility_of_element_located(SearchToursFormLocators.start_date))
        self.driver.execute_script(
            "arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input', {bubbles: true})); arguments[0].dispatchEvent(new Event('change', {bubbles: true}));",
            date_input, date_value
        )

    @allure.step("Setting number of adults to '{1}'")
    def set_adults_number(self, adults_num):
        set_travellers_number(self.driver, adults_num, SearchToursFormLocators,
                              ["adults", "children", "travelers"])

    @allure.step("Performing search")
    def search_perform(self):
        self.wait.until(EC.element_to_be_clickable(SearchToursFormLocators.search_btn)).click()
        allure.attach(self.driver.get_screenshot_as_png(), name="search_results", attachment_type=AttachmentType.PNG)
