# test/src/database.py

import json
from typing import List
from src.endpoint import Endpoint, EndpointGroup

def load_endpoint_groups(json_file: str) -> List[EndpointGroup]:

    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    groups: List[EndpointGroup] = []

    for group_name, group_data in data.items():
        routes = group_data.get("routes", {})
        description = group_data.get("description", "")
        endpoints_list: List[Endpoint] = []

        for route_name, route_data in routes.items():
            ep = Endpoint(
                route_name=route_name,
                url=route_data.get("url", ""),
                method=route_data.get("method", "GET"),
                params=route_data.get("params", {}),
                description=description
            )
            endpoints_list.append(ep)

        group = EndpointGroup(name=group_name, endpoints=endpoints_list, description=description)
        groups.append(group)

    return groups
