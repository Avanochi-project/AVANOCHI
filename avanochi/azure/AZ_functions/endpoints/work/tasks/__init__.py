# work/tasks/__init__.py

"""
HTTP-triggered Azure Function for basic task management (Phase 1).
Provides:
 - POST /tasks        -> create a new task (requires title + user_id)
 - GET  /tasks        -> list tasks (optional ?user_id=...)
 - PATCH /tasks/{id}  -> partial update (used to mark as completed)
"""

import json
import logging
import azure.functions as func

from _shared.database import DatabaseError
from _shared.services.service_factory import ServiceFactory

# Initialize service once (through the factory)
factory = ServiceFactory()
task_service = factory.get_task_service()

def _json_response(payload, status_code=200):
    # Helper to build JSON responses consistently.
    return func.HttpResponse(
        json.dumps(payload, ensure_ascii=False),
        status_code=status_code,
        mimetype="application/json"
    )


def main(req: func.HttpRequest) -> func.HttpResponse:
    
    # Entry point for the Azure Function.
    # Supports GET, POST and PATCH (partial updates).

    logging.info(f"Tasks function invoked. Method={req.method}")

    try:
        if req.method == "POST":
            # Create a new task
            try:
                data = req.get_json()
            except ValueError:
                return _json_response({"error": "Invalid JSON payload"}, 400)

            title = (data.get("title") or "").strip()
            user_id = data.get("user_id")

            try:
                created = task_service.create_task(user_id, title)
                return _json_response(created, 201)
            except ValueError as ve:
                return _json_response({"error": str(ve)}, 400)
            except DatabaseError as e:
                logging.exception("Database error while creating task")
                return _json_response({"error": str(e)}, 500)

        elif req.method == "GET":
            # List tasks, optionally filtered by user_id
            user_id = req.params.get("user_id")
            try:
                items = task_service.list_tasks(user_id)
                return _json_response(items, 200)
            except DatabaseError as e:
                logging.exception("Database error while listing tasks")
                return _json_response({"error": str(e)}, 500)

        elif req.method == "PATCH":
            # Partial update — used to mark a task as completed.
            task_id = req.route_params.get("id") or req.params.get("id")
            if not task_id:
                return _json_response(
                    {"error": "Task id is required in route (tasks/{id})"}, 400
                )

            try:
                updated = task_service.complete_task(task_id)
                return _json_response(updated, 200)
            except DatabaseError as e:
                msg = str(e)
                logging.exception(f"Error completing task {task_id}")
                if "not found" in msg.lower():
                    return _json_response({"error": msg}, 404)
                return _json_response({"error": msg}, 500)

        else:
            return _json_response({"error": f"Method {req.method} not allowed"}, 405)

    except Exception as e:
        logging.exception("Unexpected error in tasks function")
        return _json_response(
            {"error": "Internal server error", "detail": str(e)}, 500
        )
