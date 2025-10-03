# work/work_sessions/__init__.py

"""
HTTP-triggered Azure Function for work session management (Phase 1).
Provides:
 - POST /work_sessions/start        -> start a work session
 - POST /work_sessions/end/{id}     -> end a work session
 - GET  /work_sessions/active       -> get active session for a user
"""

import json
import logging
import azure.functions as func

from _shared.database import DatabaseError
from _shared.services.service_factory import ServiceFactory


# Initialize service factory (reused across invocations)
factory = ServiceFactory()
ws_service = factory.get_work_session_service()
auth_service = factory.get_auth_service()

def _json_response(payload, status_code=200):
    # Helper to build JSON responses consistently.
    return func.HttpResponse(
        json.dumps(payload, ensure_ascii=False),
        status_code=status_code,
        mimetype="application/json"
    )

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info(f"WorkSessions function invoked. Method={req.method}")
    
    # AUTHENTICATION
    if not auth_service.validate_token(req):
        return _json_response({"error": "Unauthorized"}, 401)
    
    try:
        route = req.route_params.get("route") or ""

        # --- Start session ---
        if req.method == "POST" and route == "start":

            user_id = auth_service.validate_token(req)
            if not user_id:
                return _json_response({"error": "Field 'user_id' is required"}, 400)

            # Ensure no active session exists
            active = ws_service.get_active_session(user_id)
            if active:
                return _json_response({"error": "Active session already exists"}, 400)

            try:
                session = ws_service.start_session(user_id)
                return _json_response(
                {
                    "session_id": session["id"],
                    "start_time": session["start_time"]
                }
                , 201)
            except DatabaseError as e:
                logging.exception("Database error while starting session")
                return _json_response({"error": str(e)}, 500)

        # --- End session ---
        elif req.method == "POST" and route == "end":

            try:
                data = req.get_json()
            except ValueError:
                return _json_response({"error": "Invalid JSON payload"}, 400)
            
            session_id = data.get("session_id")
            try:
                ended = ws_service.end_session(session_id)
                return _json_response(
                {
                    "session_id": ended["id"]
                }
                , 200)
            except DatabaseError as e:
                msg = str(e)
                logging.exception(f"Error ending session {session_id}")
                if "not found" in msg.lower():
                    return _json_response({"error": msg}, 404)
                return _json_response({"error": msg}, 500)

        # --- Get active session ---
        elif req.method == "GET" and route == "active":
            user_id = auth_service.validate_token(req)
            if not user_id:
                return _json_response({"error": "Query parameter 'user_id' is required"}, 400)

            try:
                active = ws_service.get_active_session(user_id)
                if active:
                    return _json_response(
                    {
                        "session_id": active["id"],
                        "user_id": active["user_id"],
                        "start_time": active["start_time"],
                        "end_time": active["end_time"] or None,
                    }
                    , 200)
                else:
                    return _json_response({"active": False}, 200)
            except DatabaseError as e:
                logging.exception("Database error while checking active session")
                return _json_response({"error": str(e)}, 500)

        else:
            return _json_response({"error": f"Method {req.method} with route not supported"}, 405)

    except Exception as e:
        logging.exception("Unexpected error in work_sessions function")
        return _json_response(
            {"error": "Internal server error", "detail": str(e)}, 500
        )
