import allure
from allure_commons.types import AttachmentType
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators.locators import SearchFlightsFormLocators


class SearchFlightsForm:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    @allure.step("Opening phptravels.net flights page")
    def open_page(self):
        self.driver.get("https://phptravels.net/flights")

    @allure.step("Setting location from: '{loc_from}'")
    def set_loc_from(self, loc_from):
        from_input = self.wait.until(EC.element_to_be_clickable(SearchFlightsFormLocators.from_input))
        from_input.clear()
        from_input.send_keys(loc_from)

    @allure.step("Setting location to: '{loc_to}'")
    def set_loc_to(self, loc_to):
        to_input = self.wait.until(EC.element_to_be_clickable(SearchFlightsFormLocators.to_input))
        to_input.clear()
        to_input.send_keys(loc_to)

    @allure.step("Setting departure date to '{departure_date}'")
    def set_departure_date(self, departure_date):
        # Convert from DD/MM/YYYY to DD-MM-YYYY format
        if '/' in departure_date:
            parts = departure_date.split('/')
            departure_date = f"{parts[0]}-{parts[1]}-{parts[2]}"
        
        # Set the date via JavaScript since the input is readonly
        self.driver.execute_script(f"""
            const dateInput = document.querySelector('input[placeholder="Departure Date"]');
            if (dateInput) {{
                dateInput.value = '{departure_date}';
                dateInput.dispatchEvent(new Event('change', {{ bubbles: true }}));
                dateInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
            }}
        """)

    @allure.step("Setting return date to '{return_date}'")
    def set_return_date(self, return_date):
        # Convert from DD/MM/YYYY to DD-MM-YYYY format
        if '/' in return_date:
            parts = return_date.split('/')
            return_date = f"{parts[0]}-{parts[1]}-{parts[2]}"
        
        # Set the date via JavaScript since the input is readonly
        self.driver.execute_script(f"""
            const dateInput = document.querySelector('input[placeholder="Return Date"]');
            if (dateInput) {{
                dateInput.value = '{return_date}';
                dateInput.dispatchEvent(new Event('change', {{ bubbles: true }}));
                dateInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
            }}
        """)

    @allure.step("Setting number of adults to '{adults_num}'")
    def set_adults_number(self, adults_num):
        # This is a hidden field, so we need to set it via JavaScript
        self.driver.execute_script(f"document.querySelector('input[name=\"adults\"]').value = '{adults_num}';")

    @allure.step("Setting number of children to '{children_num}'")
    def set_children_number(self, children_num):
        # This is a hidden field, so we need to set it via JavaScript
        self.driver.execute_script(f"document.querySelector('input[name=\"children\"]').value = '{children_num}';")

    @allure.step("Setting number of infants to '{infants_num}'")
    def set_infants_number(self, infants_num):
        # This is a hidden field, so we need to set it via JavaScript
        self.driver.execute_script(f"document.querySelector('input[name=\"infants\"]').value = '{infants_num}';")

    @allure.step("Performing search")
    def search_perform(self):
        search_btn = self.wait.until(EC.element_to_be_clickable(SearchFlightsFormLocators.search_btn))
        search_btn.click()
        allure.attach(self.driver.get_screenshot_as_png(), name="search_results", attachment_type=AttachmentType.PNG)

    @allure.step("Getting input start date")
    def get_start_date(self):
        start_date = self.driver.find_element(*SearchFlightsFormLocators.flight_date_start)
        start_date_val = start_date.get_attribute("value")

    @allure.step("Getting input end date")
    def get_end_date(self):
        end_date = self.driver.find_element(*SearchFlightsFormLocators.flight_date_end)
        end_date_val = end_date.get_attribute("value")
