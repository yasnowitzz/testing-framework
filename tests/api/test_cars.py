"""
API Cars Tests - Testing API Ninjas Cars API
"""
import pytest
import allure
from src.api.endpoints import APIEndpoints
from src.api.schemas import validate_cars_response


@allure.feature("Cars API")
class TestCarsAPI:
    @pytest.fixture(scope="class")
    def api_ninjas(self, api_client_factory):
        return api_client_factory("api_ninjas")

    @allure.story("Each car must have a specified make and model")
    @pytest.mark.api
    @pytest.mark.xfail(reason="Known issue: API returns 400 instead of 200")
    def test_each_car_must_have_a_specified_make_and_model(self, api_ninjas):
        with allure.step("Search for all cars"):
            response = api_ninjas.get(APIEndpoints.CARS)

            assert response.status_code == 200
            cars_data = response.json()

            # Verify response structure and contract validation
            assert isinstance(cars_data, list)
            assert len(cars_data) > 0
            validate_cars_response(cars_data)

    @allure.story("All Toyotas from 2023 must have a value for the displacement field")
    @pytest.mark.api
    def test_all_toyotas_from_2023_must_have_a_value_for_the_displacement_field(
        self, api_ninjas
    ):
        with allure.step("Search for all Toyotas from 2023"):
            response = api_ninjas.get(
                APIEndpoints.CARS, params={"year": 2023, "make": "Toyota"}
            )

            assert response.status_code == 200
            cars_data = response.json()

            # Verify response structure and contract validation
            assert isinstance(cars_data, list)
            assert len(cars_data) > 0
            validate_cars_response(cars_data)

            # Verify car data every toyota from 2023 has a value for the displacement field
            for car in cars_data:
                assert "displacement" in car
                assert car["displacement"] is not None
                assert car["make"].lower() == "toyota"
                assert car["year"] == 2023

    @allure.story(
        "All Toyota, Lexus, and Hyundai electric cars must not include cylinder information"
    )
    @pytest.mark.api
    @pytest.mark.parametrize("make", [("Toyota"), ("Lexus"), ("Hyundai")])
    def test_all_toyota_lexus_and_hyundai_electric_cars_must_not_include_cylinder_information(
        self, api_ninjas, make
    ):
        with allure.step(f"Search for all {make} electric cars"):
            response = api_ninjas.get(
                APIEndpoints.CARS, params={"make": make, "fuel_type": "electric"}
            )

            assert response.status_code == 200
            cars_data = response.json()

            # Verify response structure and contract validation
            assert isinstance(cars_data, list)
            validate_cars_response(cars_data)

            # Check that electric cars don't have cylinder information
            for car in cars_data:
                assert car["make"].lower() == make.lower()
                assert (
                    "cylinders" not in car or car["cylinders"] is None
                ), f"Electric {make} should not have cylinder information"

    @allure.story("Cars endpoint needs authentication api key")
    @pytest.mark.api
    def test_cars_endpoint_needs_authentication_api_key(self, api_client_factory):
        api_ninjas = api_client_factory("api_ninjas")

        with allure.step("Missing api key"):
            response = api_ninjas.get(APIEndpoints.CARS, use_auth=False)

            assert response.status_code == 400
            assert response.json()["error"] == "Missing API Key."

    @allure.story("Cars endpoint needs valid api key")
    @pytest.mark.api
    def test_cars_endpoint_needs_valid_api_key(self, api_client_factory):
        api_ninjas = api_client_factory(service_name="api_ninjas")
        api_ninjas.set_api_key("invalid")

        with allure.step("Invalid api key"):
            response = api_ninjas.get(
                APIEndpoints.CARS,
            )

            assert response.status_code == 400
            assert response.json()["error"] == "Invalid API Key."
