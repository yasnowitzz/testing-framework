import pytest
import allure
from src.utils.config import Config

# Import fixtures from other modules
from src.api.client import APIClient


@pytest.fixture(scope="session")
def config():
    """Get configuration"""
    config = Config.load()
    return config


@pytest.fixture(scope="module")
def api_ninjas(config):
    api_ninjas = APIClient(config.api_ninjas.base_url)
    api_ninjas.set_api_key(config.api_ninjas.api_key)
    return api_ninjas


def pytest_runtest_setup(item):
    """Setup before each test"""
    # Add test name to Allure
    allure.dynamic.testcase(item.name)


def pytest_runtest_teardown(item, nextitem):
    """Teardown after each test"""
    pass
