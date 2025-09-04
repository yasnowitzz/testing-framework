"""
API Cars Tests - Testing API Ninjas Cars API
"""
import pytest
import allure
import jsonschema
from src.api.endpoints import APIEndpoints
from src.api.schemas import CAR_SCHEMA, CARS_RESPONSE_SCHEMA, validate_car_data, validate_cars_response


@allure.feature("Cars API")
class TestCarsAPI:
    """Test Cars API functionality from API Ninjas"""
    
    @allure.story("Search Cars")
    @pytest.mark.api
    def test_search_cars_by_model(self, api_client_factory):
        """Test searching cars by model (Camry)"""
        cars_client = api_client_factory("api_ninjas")
        
        with allure.step("Search for Camry cars"):
            response = cars_client.get(
                APIEndpoints.CARS,
                params={"model": "camry"}
            )
            
            assert response.status_code == 200
            cars_data = response.json()
            
            # Verify response structure
            assert isinstance(cars_data, list)
            assert len(cars_data) > 0
            
            # Verify car data structure
            car = cars_data[0]
            assert "make" in car
            assert "model" in car
            assert "year" in car
            
            # Verify it's a Camry
            assert car["model"].lower() == "camry"
