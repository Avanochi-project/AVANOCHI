# work/stats/__init__.py
"""
HTTP-triggered Azure Function for statistics (Phase 1).
Provides:
 - GET /stats/{user_id} -> hours worked + tasks completed
"""

import json
import logging
import azure.functions as func

from _shared.credential_manager import CredentialManager
from _shared.database import CosmosDBService, DatabaseError
from _shared.repos.task_repo import TaskRepository
from _shared.repos.work_session_repo import WorkSessionRepository


# Initialize dependencies
cred_manager = CredentialManager()
db_service = CosmosDBService(cred_manager)
task_repo = TaskRepository(db_service)
ws_repo = WorkSessionRepository(db_service)


def _json_response(payload, status_code=200):
    return func.HttpResponse(
        json.dumps(payload, ensure_ascii=False),
        status_code=status_code,
        mimetype="application/json"
    )


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info(f"Stats function invoked. Method={req.method}")

    if req.method != "GET":
        return _json_response({"error": f"Method {req.method} not allowed"}, 405)

    user_id = req.route_params.get("user_id") or req.params.get("user_id")
    if not user_id:
        return _json_response({"error": "user_id is required in route or query"}, 400)

    try:
        # --- Hours worked ---
        sessions = ws_repo.list_sessions(user_id)
        total_hours = 0.0
        for s in sessions:
            if s.get("duration") is not None:
                total_hours += float(s["duration"])

        # --- Tasks completed ---
        query = "SELECT VALUE COUNT(1) FROM c WHERE c.type = @type AND c.user_id = @user_id AND c.completed = true"
        params = [
            {"name": "@type", "value": "task"},
            {"name": "@user_id", "value": user_id}
        ]
        result = task_repo.query(query, params)
        tasks_completed = result[0] if result else 0

        stats = {
            "user_id": user_id,
            "hours_worked": round(total_hours, 2),
            "tasks_completed": tasks_completed
        }

        return _json_response(stats, 200)

    except DatabaseError as e:
        logging.exception("Database error while generating stats")
        return _json_response({"error": str(e)}, 500)
    except Exception as e:
        logging.exception("Unexpected error in stats function")
        return _json_response({"error": "Internal server error", "detail": str(e)}, 500)
