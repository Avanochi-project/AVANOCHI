# main.py

from src.database import load_endpoint_groups
from src.uix import select_endpoint_group, select_endpoint, fill_endpoint_body, clear_screen
from src.http_client import HttpClient

def main():
    """
    Main workflow for local endpoint testing tool.
    1. Load endpoint groups from JSON
    2. Interactive ASCII menu for group, endpoint, and body input
    3. Send HTTP request and display response
    """
    # Load endpoint groups
    clear_screen()
    domain_groups = load_endpoint_groups("endpoints.json")

    # Create HTTP client (base_url can be empty if endpoints have full URL)
    client = HttpClient()

    while True:
        # ===== Level 1: Select EndpointGroup =====
        group_idx = select_endpoint_group(domain_groups)
        selected_group = domain_groups[group_idx]

        # ===== Level 2: Select Endpoint =====
        endpoint_idx = select_endpoint(selected_group)
        selected_endpoint = selected_group.endpoints[endpoint_idx]

        # ===== Level 3: Fill body inputs =====
        body_data = fill_endpoint_body(selected_endpoint)

        # Prepare URL and body
        url = selected_endpoint.prepare_url(body_data)
        body = selected_endpoint.prepare_body(body_data)

        print("\nDEBUG: sending body:", body)
        print("DEBUG: to URL:", url)

        # Send HTTP request based on method
        method = selected_endpoint.method.upper()
        try:
            if method == "GET":
                response = client.get(url)
            elif method == "POST":
                response = client.post(url, json=body)
            elif method == "PUT":
                response = client.put(url, json=body)
            elif method == "DELETE":
                response = client.delete(url, json=body)
            else:
                print(f"Unsupported HTTP method: {method}")
                continue

            # Try to display JSON response, fallback to text
            try:
                print("\nResponse from endpoint:")
                print(response.json())
            except Exception:
                print(response.text)

        except Exception as e:
            print(f"\nRequest failed: {e}")

        # Ask user if they want to continue
        cont = input("\nDo you want to continue? (y/n): ").lower()
        if cont != "y":
            print("Exiting...")
            break


if __name__ == "__main__":
    main()
