"""
API Cars Tests - Testing API Ninjas Cars API
"""
import pytest
import allure
from src.api.endpoints import APIEndpoints
from src.api.client import APIClient
from src.api.schemas import validate_vin_response


@allure.feature("VIN API")
class TestVINAPI:
    """Test VIN API functionality from API Ninjas"""

    @allure.story("VIN endpoint returns data in the same structure as sample VINs")
    @pytest.mark.api
    @pytest.mark.parametrize(
        "vin",
        [
            "JT3HP10VXW7092383",
            "4TARN13P1SZ314855",
            "JTDKN3DU6C1423122",
            "KMHDN45D32D464848",
        ],
    )
    def test_vin_endpoint_returns_data_in_the_same_structure_as_sample_vins(
        self, api_ninjas, vin
    ):
        vin = vin

        with allure.step("Specific VIN lookup"):
            response = api_ninjas.get(APIEndpoints.VIN, params={"vin": vin})

            assert response.status_code == 200
            vin_data = response.json()

            # Verify response structure and contract validation
            assert isinstance(vin_data, dict)
            validate_vin_response(vin_data)

            assert vin_data["vin"] == vin

    @allure.story("VIN param must have 17 characters")
    @pytest.mark.api
    @pytest.mark.parametrize("vin", ["JH4KA7561PC00826", "JH4KA7561PC0082690"])
    def test_vin_param_must_have_17_characters(self, api_ninjas, vin):
        with allure.step("Invalid VIN lookup"):
            response = api_ninjas.get(APIEndpoints.VIN, params={"vin": vin})

            assert response.status_code == 400
            assert (
                response.json()["error"]
                == "Failed to look up VIN. Please make sure to input a valid 17-character VIN."
            )

    @allure.story("VIN endpoint requieres vin param")
    @pytest.mark.api
    def test_vin_endpoint_requieres_vin_param(self, api_ninjas):
        with allure.step("VIN lookup without vin param"):
            response = api_ninjas.get(APIEndpoints.VIN, params={})

            assert response.status_code == 400
            assert response.json()["error"] == "vin parameter must be provided."

    @allure.story("VIN endpoint needs authentication api key")
    @pytest.mark.api
    def test_vin_endpoint_needs_authentication_api_key(self, config):
        api_ninjas = APIClient(base_url=config.api_ninjas.base_url)

        with allure.step("Missing api key"):
            response = api_ninjas.get(
                APIEndpoints.VIN, params={"vin": "JH4KA7561PC008269"}, use_auth=False
            )

            assert response.status_code == 400
            assert response.json()["error"] == "Missing API Key."

    @allure.story("VIN endpoint needs valid api key")
    @pytest.mark.api
    def test_vin_endpoint_needs_valid_api_key(self, config):
        api_ninjas = APIClient(base_url=config.api_ninjas.base_url)
        api_ninjas.set_api_key("invalid")

        with allure.step("Invalid api key"):
            response = api_ninjas.get(
                APIEndpoints.VIN, params={"vin": "JH4KA7561PC008269"}
            )

            assert response.status_code == 400
            assert response.json()["error"] == "Invalid API Key."
