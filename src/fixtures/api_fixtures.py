"""
API-specific fixtures
"""
import pytest
from src.api.client import APIClient
from typing import Optional


@pytest.fixture(scope="function")
def api_client_factory(config):
    def create_client(service_name=None, base_url=None, api_key=None):
        if service_name:
            # Użyj generic method
            url, key = config.get_api_config(service_name)
            if not url:
                raise ValueError(f"Unknown service: {service_name}")
        else:
            url = base_url
            key = api_key
        
        client = APIClient(url)
        if key:
            client.set_api_key(key)
        return client
    
    return create_client
