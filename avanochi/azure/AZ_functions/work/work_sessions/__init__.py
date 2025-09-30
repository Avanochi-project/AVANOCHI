# work/work_sessions/__init__.py
"""
HTTP-triggered Azure Function for work session management (Phase 1).
Provides:
 - POST /work_sessions/start        -> start a work session
 - POST /work_sessions/{id}/end     -> end a work session
 - GET  /work_sessions/active       -> get active session for a user
"""

import json
import logging
import azure.functions as func

from _shared.credential_manager import CredentialManager
from _shared.database import CosmosDBService, DatabaseError
from _shared.repos.work_session_repository import WorkSessionRepository
from _shared.services.work_session_service import WorkSessionService
from _shared.entities.work_session import WorkSession


# Initialize dependencies (reused across invocations)
cred_manager = CredentialManager()
db_service = CosmosDBService(cred_manager)
ws_repo = WorkSessionRepository(db_service)
ws_service = WorkSessionService(ws_repo)


def _json_response(payload, status_code=200):
    """Helper to build JSON responses consistently."""
    return func.HttpResponse(
        json.dumps(payload, ensure_ascii=False),
        status_code=status_code,
        mimetype="application/json"
    )


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info(f"WorkSessions function invoked. Method={req.method}")

    try:
        # Route handling
        route = req.route_params.get("id") or ""
        action = req.route_params.get("action") or ""

        if req.method == "POST" and route == "start":
            # POST /work_sessions/start
            try:
                data = req.get_json()
            except ValueError:
                return _json_response({"error": "Invalid JSON payload"}, 400)

            user_id = data.get("user_id")
            if not user_id:
                return _json_response({"error": "Field 'user_id' is required"}, 400)

            # Check if an active session already exists
            active = ws_service.get_active_session(user_id)
            if active:
                return _json_response({"error": "Active session already exists"}, 400)

            try:
                session = ws_service.start_session(user_id)
                return _json_response(session, 201)
            except DatabaseError as e:
                logging.exception("Database error while starting session")
                return _json_response({"error": str(e)}, 500)

        elif req.method == "POST" and route:
            # POST /work_sessions/{id}/end
            session_id = route
            try:
                ended = ws_service.end_session(session_id)
                return _json_response(ended, 200)
            except DatabaseError as e:
                msg = str(e)
                logging.exception(f"Error ending session {session_id}")
                if "not found" in msg.lower():
                    return _json_response({"error": msg}, 404)
                return _json_response({"error": msg}, 500)

        elif req.method == "GET" and route == "active":
            # GET /work_sessions/active?user_id=xxx
            user_id = req.params.get("user_id")
            if not user_id:
                return _json_response({"error": "Query parameter 'user_id' is required"}, 400)

            try:
                active = ws_service.get_active_session(user_id)
                if active:
                    return _json_response(active, 200)
                else:
                    return _json_response({"active": False}, 200)
            except DatabaseError as e:
                logging.exception("Database error while checking active session")
                return _json_response({"error": str(e)}, 500)

        else:
            return _json_response({"error": f"Method {req.method} with route not supported"}, 405)

    except Exception as e:
        logging.exception("Unexpected error in work_sessions function")
        return _json_response({"error": "Internal server error", "detail": str(e)}, 500)
