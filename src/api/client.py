import requests
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class APIClient:
    """
    HTTP Client for API testing with authentication support
    Supports both Bearer token (from login) and X-API-Key authentication
    """

    def __init__(self, base_url: str, timeout: int = 30):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.api_key = None

        # Default headers
        self.session.headers.update(
            {"Content-Type": "application/json", "Accept": "application/json"}
        )

    def set_api_key(self, api_key: str) -> None:
        """
        Set X-API-Key header for authentication

        Args:
            api_key: API key string
        """
        self.api_key = api_key
        self.session.headers.update({"X-API-Key": api_key})
        logger.info("API Key authentication set")

    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        use_auth: bool = True,
    ) -> requests.Response:
        """
        Make HTTP request

        Args:
            method: HTTP method (GET, POST, PUT, DELETE, etc.)
            endpoint: API endpoint
            data: Request body data
            params: Query parameters
            headers: Additional headers
            use_auth: Whether to use authentication

        Returns:
            requests.Response: HTTP response
        """
        url = f"{self.base_url}{endpoint}"

        # Prepare headers
        request_headers = {}
        if headers:
            request_headers.update(headers)

        # Prepare session (with or without auth)
        session = self.session
        if not use_auth:
            # Create temporary session without auth
            session = requests.Session()
            session.headers.update(self.session.headers)
            if "X-API-Key" in session.headers:
                del session.headers["X-API-Key"]

        # Make request
        try:
            response = session.request(
                method=method.upper(),
                url=url,
                json=data,
                params=params,
                headers=request_headers,
                timeout=self.timeout,
            )

            # Log request details
            logger.info(f"{method.upper()} {url} - Status: {response.status_code}")

            return response

        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            raise

    def get(
        self, endpoint: str, params: Optional[Dict[str, Any]] = None, **kwargs
    ) -> requests.Response:
        """GET request"""
        return self._make_request("GET", endpoint, params=params, **kwargs)

    def post(
        self, endpoint: str, data: Optional[Dict[str, Any]] = None, **kwargs
    ) -> requests.Response:
        """POST request"""
        return self._make_request("POST", endpoint, data=data, **kwargs)

    def put(
        self, endpoint: str, data: Optional[Dict[str, Any]] = None, **kwargs
    ) -> requests.Response:
        """PUT request"""
        return self._make_request("PUT", endpoint, data=data, **kwargs)

    def patch(
        self, endpoint: str, data: Optional[Dict[str, Any]] = None, **kwargs
    ) -> requests.Response:
        """PATCH request"""
        return self._make_request("PATCH", endpoint, data=data, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        """DELETE request"""
        return self._make_request("DELETE", endpoint, **kwargs)

    def is_authenticated(self) -> bool:
        """Check if client is authenticated"""
        return bool(self.api_key)

    def get_auth_info(self) -> Dict[str, Any]:
        """Get current authentication info"""
        return {
            "has_api_key": bool(self.api_key),
            "api_key_preview": f"{self.api_key[:10]}..." if self.api_key else None,
        }
