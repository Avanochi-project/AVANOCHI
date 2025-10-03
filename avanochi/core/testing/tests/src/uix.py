# test/src/uix.py

import json
import os
from typing import List, Dict, Any, Optional
from src.endpoint import Endpoint, EndpointGroup

def clear_screen():
    # Clear terminal screen, cross-platform.
    os.system("cls" if os.name == "nt" else "clear")
    return None

def draw_panel(title: str, lines: Optional[List[str]] = None) -> None:
    # Print a simple ASCII panel with a title and optional lines of text.
    lines = lines or []  # si es None, lo convertimos en lista vacía
    width = max(len(title), *(len(line) for line in lines)) + 4 if lines else len(title) + 4

    print("+" + "-" * width + "+")
    print(f"| {title.center(width - 2)} |")
    print("+" + "-" * width + "+")

    if lines:
        for line in lines:
            print(f"| {line.ljust(width - 2)} |")
        print("+" + "-" * width + "+")

def select_endpoint_group(domain_groups: List[EndpointGroup]) -> int:

    # Level 1: Select an EndpointGroup
    # Display all endpoint groups and return the selected index.
    
    clear_screen()
    lines = [f"{idx+1}. {group.name}" for idx, group in enumerate(domain_groups)]
    draw_panel("ENDPOINTS", lines)

    while True:
        try:
            choice = int(input("SELECT: "))
            if 1 <= choice <= len(domain_groups):
                return choice - 1
        except ValueError:
            pass
        print(f"Please enter a number between 1 and {len(domain_groups)}")


def select_endpoint(group: EndpointGroup) -> int:

    # Level 2: Select an Endpoint within a group
    # Display all endpoints in a group and return the selected index.

    clear_screen()
    lines = [f"{idx+1}. {ep.route_name}" for idx, ep in enumerate(group.endpoints)]
    draw_panel(group.name, lines)

    while True:
        try:
            choice = int(input("SELECT: "))
            if 1 <= choice <= len(group.endpoints):
                return choice - 1
        except ValueError:
            pass
        print(f"Please enter a number between 1 and {len(group.endpoints)}")

def fill_endpoint_body(endpoint: Endpoint) -> Dict[str, Any]:

    # Level 3: Fill input body for the selected endpoint
    # Prompt user to fill all body fields of the endpoint.

    clear_screen()
    draw_panel(endpoint.route_name, ["Enter the following values:"])
    body_data: Dict[str, Any] = {}

    for key in endpoint.params:
        value = input(f"{key.capitalize()} [{endpoint.params[key]}]: ") or endpoint.params[key]
        body_data[key] = value

    return body_data

def print_API_response(endpoint, response_data: dict):
    """
    Pretty print the response based on the endpoint's response schema.
    Falls back to printing raw JSON if schema not available or doesn't match.
    """
    clear_screen()
    response_schema = getattr(endpoint, "response", None)
    title = f"API RESPONSE: {endpoint.route_name}"

    draw_panel(title, None)
    if not response_schema:
        # No schema provided, just dump the whole JSON nicely
        print(json.dumps(response_data, indent=4))
        return

    # Print each expected field in the schema
    for key, desc in response_schema.items():
        value = response_data.get(key, "<missing>")
        print(f"{key}: {value} ({desc})")

    print("+---------------------------+\n")
