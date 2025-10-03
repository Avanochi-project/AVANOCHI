# test/src/http_client.py

import requests
from typing import Dict, Optional, Any

class HttpClient:

    # Simple HTTP client for testing absolute URLs.

    def __init__(self):
        self.token: Optional[str] = None 

    def set_token(self, token: str):
        self.token = token  

    def _request(
        self,
        method: str,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None
    ) -> requests.Response:
        
        if headers is None:
            headers = {}
        
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        # Send an HTTP request to the absolute URL.
        try:
            response = requests.request(
                method=method.upper(),
                url=url,
                headers=headers,
                params=params,
                json=json,
                timeout=10
            )
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            raise RuntimeError(f"HTTP request failed: {e}")

    # Convenience methods
    def get(self, url: str, headers: Optional[Dict[str, str]] = None,
            params: Optional[Dict[str, Any]] = None) -> requests.Response:
        return self._request("GET", url, headers=headers, params=params)

    def post(self, url: str, headers: Optional[Dict[str, str]] = None,
             json: Optional[Dict[str, Any]] = None) -> requests.Response:
        return self._request("POST", url, headers=headers, json=json)

    def put(self, url: str, headers: Optional[Dict[str, str]] = None,
            json: Optional[Dict[str, Any]] = None) -> requests.Response:
        return self._request("PUT", url, headers=headers, json=json)

    def delete(self, url: str, headers: Optional[Dict[str, str]] = None,
               json: Optional[Dict[str, Any]] = None) -> requests.Response:
        return self._request("DELETE", url, headers=headers, json=json)

    def patch(self, url: str, headers: Optional[Dict[str, str]] = None,
            json: Optional[Dict[str, Any]] = None) -> requests.Response:
        return self._request("PATCH", url, headers=headers, json=json)
