import pytest
import allure
from src.utils.config import Config

# Import fixtures from other modules
from src.fixtures.api_fixtures import *


@pytest.fixture(scope="session")
def config():
    """Get configuration"""
    return Config()


def pytest_runtest_setup(item):
    """Setup before each test"""
    # Add test name to Allure
    allure.dynamic.testcase(item.name)


def pytest_runtest_teardown(item, nextitem):
    """Teardown after each test"""
    pass
