import pytest
import allure

from pages.phptravels.search_hotels_form import SearchHotelsForm
from utils.read_xlsx import XlsxReader


@pytest.mark.usefixtures("setup")
class TestHotelSearch:
    @allure.title("Search hotel test")
    @allure.description("This is test of searching hotel in Warsaw")
    def test_search_hotel_1(self):
        search_hotel = SearchHotelsForm(self.driver)
        search_hotel.open_page()
        search_hotel.set_destination("Warsaw")
        search_hotel.set_date_range("29/04/2025", "03/07/2026")
        search_hotel.set_adults_number(3)
        search_hotel.set_kids_number(0)
        search_hotel.set_nationality("Ethiopia")
        search_hotel.search_perform()

        # Check if we navigated to the hotel search results page
        assert "/stays/warsaw" in self.driver.current_url

    @allure.title("Search hotel test 2")
    @allure.description("This is data driven test of searching hotels")
    @pytest.mark.parametrize("data", XlsxReader.get_xlsx_hotels_data())
    def test_search_hotel_2(self, data):
        search_hotel = SearchHotelsForm(self.driver)
        search_hotel.open_page()
        search_hotel.set_destination(data.destination)
        search_hotel.set_date_range(data.check_in, data.check_out)
        search_hotel.set_adults_number(data.adults_num)
        search_hotel.set_kids_number(data.kids_num)
        search_hotel.set_nationality("Egypt")
        search_hotel.search_perform()

        assert "/stays/" in self.driver.current_url
