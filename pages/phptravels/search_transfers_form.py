import allure
from allure_commons.types import AttachmentType
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from locators.locators import SearchTransferLocators, SearchTabsLocators


class SearchTransfersForm:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    @allure.step("Opening phptravels.net cars page")
    def open_page(self):
        self.driver.get("https://phptravels.net/cars")

    @allure.step("Opening transfer tab")
    def open_transfer_tab(self):
        transfer_tab = self.wait.until(EC.element_to_be_clickable(SearchTabsLocators.transfer_tab))
        transfer_tab.click()

    @allure.step("Setting pick up location: '{pick_up_loc}'")
    def set_pick_up_loc(self, pick_up_loc):
        pickup_input = self.wait.until(EC.presence_of_element_located(SearchTransferLocators.pick_up_loc))
        pickup_input.clear()
        pickup_input.send_keys(pick_up_loc)

    @allure.step("Setting drop off location: '{drop_off_loc}'")
    def set_drop_off_loc(self, drop_off_loc):
        dropoff_input = self.wait.until(EC.presence_of_element_located(SearchTransferLocators.drop_off_loc))
        dropoff_input.clear()
        dropoff_input.send_keys(drop_off_loc)

    @allure.step("Setting pick-up date to '{pickup_date}'")
    def set_pickup_date(self, pickup_date):
        # Convert from DD/MM/YYYY to DD-MM-YYYY format if needed
        if '/' in pickup_date:
            parts = pickup_date.split('/')
            pickup_date = f"{parts[0]}-{parts[1]}-{parts[2]}"
        
        # Set the date via JavaScript since it might be readonly
        self.driver.execute_script(f"""
            const dateInput = document.querySelector('input[name="pickup_date"]');
            if (dateInput) {{
                dateInput.value = '{pickup_date}';
                dateInput.dispatchEvent(new Event('change', {{ bubbles: true }}));
                dateInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
            }}
        """)

    @allure.step("Setting pick-up time to '{pickup_time}'")
    def set_pickup_time(self, pickup_time):
        # Set the time via JavaScript
        self.driver.execute_script(f"""
            const timeInput = document.querySelector('input[name="pickup_time"]');
            if (timeInput) {{
                timeInput.value = '{pickup_time}';
                timeInput.dispatchEvent(new Event('change', {{ bubbles: true }}));
                timeInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
            }}
        """)

    @allure.step("Setting return date to '{return_date}'")
    def set_return_date_value(self, return_date):
        # Convert from DD/MM/YYYY to DD-MM-YYYY format if needed
        if '/' in return_date:
            parts = return_date.split('/')
            return_date = f"{parts[0]}-{parts[1]}-{parts[2]}"
        
        # Set the date via JavaScript since it might be readonly
        self.driver.execute_script(f"""
            const dateInput = document.querySelector('input[name="return_date"]');
            if (dateInput) {{
                dateInput.value = '{return_date}';
                dateInput.dispatchEvent(new Event('change', {{ bubbles: true }}));
                dateInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
            }}
        """)

    @allure.step("Setting return time to '{return_time}'")
    def set_return_time_value(self, return_time):
        # Set the time via JavaScript
        self.driver.execute_script(f"""
            const timeInput = document.querySelector('input[name="return_time"]');
            if (timeInput) {{
                timeInput.value = '{return_time}';
                timeInput.dispatchEvent(new Event('change', {{ bubbles: true }}));
                timeInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
            }}
        """)

    # Legacy methods for backward compatibility with tests
    @allure.step("Setting depart date to '{start_year}'/'{start_month}'/'{start_day}'")
    def set_depart_date(self, start_year, start_month, start_day):
        # Convert to DD-MM-YYYY format
        month_map = {
            'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06',
            'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'
        }
        month_num = month_map.get(start_month, '01')
        pickup_date = f"{start_day}-{month_num}-{start_year}"
        self.set_pickup_date(pickup_date)

    @allure.step("Setting depart time to '{depart_time}'")
    def set_depart_time(self, depart_time):
        self.set_pickup_time(depart_time)

    @allure.step("Setting return date to '{end_year}'/'{end_month}'/'{end_day}'")
    def set_return_date(self, end_year, end_month, end_day):
        # Convert to DD-MM-YYYY format
        month_map = {
            'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06',
            'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'
        }
        month_num = month_map.get(end_month, '01')
        return_date = f"{end_day}-{month_num}-{end_year}"
        self.set_return_date_value(return_date)

    @allure.step("Setting return time to '{return_time}'")
    def set_return_time(self, return_time):
        self.set_return_time_value(return_time)

    @allure.step("Performing search")
    def search_perform(self):
        search_btn = self.wait.until(EC.presence_of_element_located(SearchTransferLocators.search_btn))
        search_btn.click()
        allure.attach(self.driver.get_screenshot_as_png(), name="search_results", attachment_type=AttachmentType.PNG)
