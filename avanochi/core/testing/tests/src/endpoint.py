# src/endpoint.py

from typing import List, Dict, Any, Optional

class Endpoint:
    def __init__(
        self,
        route_name: str,
        url: str,
        method: str,
        params: Optional[Dict[str, Any]] = None,
        response: Optional[Dict[str, Any]] = None,
        description: str = ""
    ):
        self.route_name = route_name
        self.url = url
        self.method = method.upper()
        self.params = params or {}
        self.response = response or {}
        self.description = description

    def prepare_url(self, inputs: Dict[str, Any]) -> str:
        final_url = self.url
        for key, value in inputs.items():
            final_url = final_url.replace(f"{{{key}}}", str(value))
        return final_url

    def prepare_params(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        final_params = {}
        for key in self.params:
            if key in inputs:
                final_params[key] = inputs[key]
        return final_params
    
    def __str__(self):
        return f"{self.route_name} [{self.method}] {self.url}"

class EndpointGroup:

    def __init__(self, name: str, endpoints: List[Endpoint], description: str = ""):
        self.name = name
        self.endpoints = endpoints
        self.description = description

    def __str__(self):
        return f"{self.name} ({len(self.endpoints)} routes)"
