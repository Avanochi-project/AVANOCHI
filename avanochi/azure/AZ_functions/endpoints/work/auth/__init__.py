# endpoints/work/auth/__init__.py

"""
HTTP-triggered Azure Function for user authentication.
Provides:
 - POST /auth/register   -> register a new user
 - POST /auth/login      -> authenticate a user and return a JWT
 - GET  /auth/user_info  -> get user info (requires valid JWT in headers or cookies)
"""

import json
import logging
import azure.functions as func

from _shared.database import DatabaseError
from _shared.services.service_factory import ServiceFactory

# Initialize service once
factory = ServiceFactory()
auth_service = factory.get_auth_service()

def _json_response(payload, status_code=200):
    """Helper to build JSON responses consistently."""
    return func.HttpResponse(
        json.dumps(payload, ensure_ascii=False),
        status_code=status_code,
        mimetype="application/json"
    )

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info(f"Auth function invoked. Method={req.method}")

    try:
        if req.method == "POST":

            route = req.route_params.get("action")

            # --- Register new user ---
            if route == "register":
                try:
                    data = req.get_json()
                except ValueError:
                    return _json_response({"error": "Invalid JSON payload"}, 400)

                username = data.get("username")
                password = data.get("password")

                if not username or not password:
                    return _json_response({"error": "Fields 'username' and 'password' are required"}, 400)

                try:
                    user = auth_service.register(username, password)
                    return _json_response(
                    {
                        "message": "User registered successfully", 
                        "user": user["id"]
                    }
                    , 201)
                except ValueError as e:
                    return _json_response({"error": str(e)}, 400)
                except DatabaseError as e:
                    logging.exception("Database error while registering user")
                    return _json_response({"error": str(e)}, 500)

            # --- Login ---
            elif route == "login":
                try:
                    data = req.get_json()
                except ValueError:
                    return _json_response({"error": "Invalid JSON payload"}, 400)

                username = data.get("username")
                password = data.get("password")

                if not username or not password:
                    return _json_response({"error": "Fields 'username' and 'password' are required"}, 400)

                try:
                    token = auth_service.login(username, password)
                    return _json_response(
                    {
                        "token": token
                    }
                    , 200)
                except ValueError as e:
                    return _json_response({"error": str(e)}, 401)
                except DatabaseError as e:
                    logging.exception("Database error while logging in user")
                    return _json_response({"error": str(e)}, 500)

            else:
                return _json_response({"error": "Invalid route. Use /auth/register or /auth/login"}, 404)

        elif req.method == "GET":
            route = req.route_params.get("action")
            logging.info(f"Route param received: {route}")

            # --- Get user info ---
            if route == "user_info":
                try:
                    user_id = auth_service.validate_token(req)
                    logging.info(f"user_id extracted: {user_id}")
                    user = auth_service.get_user_by_id(user_id)
                    if not user:
                        return _json_response({"error": "User not found"}, 404)
                    return _json_response(
                    {
                        "username": user["name"],
                        "user_id": user["id"]
                    }
                    , 200)
                except ValueError as e:
                    return _json_response({"error": str(e)}, 401)
                except DatabaseError as e:
                    logging.exception("Database error while fetching user info")
                    return _json_response({"error": str(e)}, 500)

            else:
                return _json_response({"error": "Invalid route. Use /auth/user"}, 404)
            
    except Exception as e:
        logging.exception("Unexpected error in auth function")
        return _json_response({"error": "Internal server error", "detail": str(e)}, 500)
