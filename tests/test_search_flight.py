import pytest
import allure

from pages.phptravels.search_flights_form import SearchFlightsForm
from utils.read_xlsx import XlsxReader


@pytest.mark.usefixtures("setup")
class TestFlightSearch:

    @allure.title("Search flight test")
    @allure.description("This is test of searching flight")
    def test_search_flight_general(self):
        search_flight = SearchFlightsForm(self.driver)
        search_flight.open_page()
        search_flight.set_loc_from("JIMMA")
        search_flight.set_loc_to("ADDIS")
        search_flight.set_departure_date("28/04/2026")
        search_flight.set_return_date("02/06/2026")
        search_flight.set_adults_number(2)
        search_flight.set_children_number(4)
        search_flight.set_infants_number(1)
        search_flight.search_perform()

    @allure.title("Search flight test: one way")
    @allure.description("This is test of searching one way flight")
    @pytest.mark.parametrize("data", XlsxReader.get_xlsx_flights_data())
    def test_search_flight_one_way(self, data):
        search_flight = SearchFlightsForm(self.driver)
        search_flight.open_page()
        search_flight.set_loc_from(data.location_from)
        search_flight.set_loc_to(data.location_to)
        departure_date = f"{data.start_day}/{data.start_month}/{data.start_year}"
        search_flight.set_departure_date(departure_date)
        search_flight.set_adults_number(data.adults_num)
        search_flight.set_children_number(data.kids_num)
        search_flight.set_infants_number(data.infants_num)
        search_flight.search_perform()

    @allure.title("Search flight test: round trip")
    @allure.description("This is test of searching round trip flight")
    @pytest.mark.parametrize("data", XlsxReader.get_xlsx_flights_data())
    def test_search_flight_round_trip(self, data):
        search_flight = SearchFlightsForm(self.driver)
        search_flight.open_page()
        search_flight.set_loc_from(data.location_from)
        search_flight.set_loc_to(data.location_to)
        departure_date = f"{data.start_day}/{data.start_month}/{data.start_year}"
        return_date = f"{data.end_day}/{data.end_month}/{data.end_year}"
        search_flight.set_departure_date(departure_date)
        search_flight.set_return_date(return_date)
        search_flight.set_adults_number(data.adults_num)
        search_flight.set_children_number(data.kids_num)
        search_flight.set_infants_number(data.infants_num)
        search_flight.search_perform()
