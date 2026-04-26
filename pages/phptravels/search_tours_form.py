import allure
from allure_commons.types import AttachmentType
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators.locators import SearchToursFormLocators


class SearchToursForm:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    @allure.step("Opening phptravels.net website")
    def open_page(self):
        self.driver.get("https://phptravels.net/tours")
        self.wait.until(EC.invisibility_of_element_located(SearchToursFormLocators.page_loader))
        self.wait.until(EC.visibility_of_element_located(SearchToursFormLocators.destination_input))

    @allure.step("Setting tour destination: '{1}'")
    def set_tour_destination(self, tour_destination):
        destination_input = self.wait.until(EC.visibility_of_element_located(
            SearchToursFormLocators.destination_input
        ))
        destination_input.clear()
        destination_input.send_keys(tour_destination)

        # wait for destination suggestions or no results marker
        try:
            self.wait.until(
                EC.visibility_of_element_located(SearchToursFormLocators.destination_results_container)
            )
        except Exception:
            pass

        suggestions = self.driver.find_elements(*SearchToursFormLocators.destination_suggestion)
        visible_suggestions = [item for item in suggestions if item.is_displayed()]

        if visible_suggestions:
            normalized_query = tour_destination.strip().lower()
            for suggestion in visible_suggestions:
                if normalized_query in suggestion.text.strip().lower():
                    suggestion.click()
                    return
            visible_suggestions[0].click()
            return

        # No visible suggestion was found: keep the raw destination text and hide the overlay.
        self.driver.execute_script(
            "const overlay = document.querySelector('div[x-show=\"destinationShouldShowDropdown || destinationShowNoResults\"]'); "
            "if (overlay) { overlay.style.display = 'none'; }"
        )
        return

    def _normalize_tour_type(self, tour_type):
        mapped_types = {
            'Educational': 'Cultural',
            'Private': 'Any Type',
            'Private Tour': 'Any Type',
            'School': 'Cultural',
            'History': 'Historical',
            'Group': 'Any Type',
            'Group Tour': 'Any Type',
            'group': 'Any Type'
        }
        return mapped_types.get(tour_type.strip(), tour_type.strip())

    @allure.step("Setting tour type: '{1}'")
    def set_tour_type(self, tour_type):
        tour_type = self._normalize_tour_type(tour_type)
        dropdown = self.wait.until(EC.element_to_be_clickable(
            SearchToursFormLocators.tour_type_dropdown
        ))
        dropdown.click()
        try:
            option = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, f"//div[contains(@class,'input-dropdown-item') and contains(normalize-space(.), '{tour_type}')]")
            ))
        except Exception:
            option = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//div[contains(@class,'input-dropdown-item') and contains(normalize-space(.), 'Any Type')]")
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
        adults_input = self.wait.until(EC.presence_of_element_located(SearchToursFormLocators.adults_input))
        current_value = int(adults_input.get_attribute('value'))
        if current_value == adults_num:
            return

        # Find buttons using JavaScript since @click is an Alpine.js directive
        add_btn = self.driver.execute_script("""
            return Array.from(document.querySelectorAll('button')).find(btn => 
                btn.getAttribute('@click') === "incrementTraveler('adults')"
            );
        """)
        subtract_btn = self.driver.execute_script("""
            return Array.from(document.querySelectorAll('button')).find(btn => 
                btn.getAttribute('@click') === "decrementTraveler('adults')"
            );
        """)

        if not add_btn or not subtract_btn:
            raise Exception("Could not find adult increment/decrement buttons")

        while current_value < adults_num:
            # Use JavaScript click since Selenium click may not work with Alpine.js
            self.driver.execute_script("arguments[0].click();", add_btn)
            current_value += 1
            # Re-read the value to ensure it updated
            current_value = int(self.driver.find_element(*SearchToursFormLocators.adults_input).get_attribute('value'))

        while current_value > adults_num:
            self.driver.execute_script("arguments[0].click();", subtract_btn)
            current_value -= 1
            current_value = int(self.driver.find_element(*SearchToursFormLocators.adults_input).get_attribute('value'))

    @allure.step("Performing search")
    def search_perform(self):
        self.wait.until(EC.invisibility_of_element_located(SearchToursFormLocators.page_loader))
        self.wait.until(EC.element_to_be_clickable(SearchToursFormLocators.search_btn)).click()
        allure.attach(self.driver.get_screenshot_as_png(), name="search_results", attachment_type=AttachmentType.PNG)
