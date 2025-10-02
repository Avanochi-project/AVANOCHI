# src/uix.py
import os
from typing import List, Dict, Any
from src.endpoint import Endpoint, EndpointGroup

def clear_screen():
    # Clear terminal screen, cross-platform.
    os.system("cls" if os.name == "nt" else "clear")

def draw_panel(title: str, lines: List[str]) -> None:
    # Print a simple ASCII panel with a title and lines of text.
    width = max(len(title), *(len(line) for line in lines)) + 4
    print("+" + "-" * width + "+")
    print(f"| {title.center(width - 2)} |")
    print("+" + "-" * width + "+")
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

    for key in endpoint.body:
        value = input(f"{key.capitalize()} [{endpoint.body[key]}]: ") or endpoint.body[key]
        body_data[key] = value

    return body_data
