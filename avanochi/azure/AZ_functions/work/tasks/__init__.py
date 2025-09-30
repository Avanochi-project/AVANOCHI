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
from datetime import datetime

import azure.functions as func

# Infrastructure / domain imports (English code + comments)
from _shared.credential_manager import CredentialManager
from _shared.database import CosmosDBService, DatabaseError
from _shared.repos.task_repo import TaskRepository
from _shared.services.task_service import TaskService
from _shared.entities.task import Task


# Module-level initialization to reuse clients across invocations when possible.
# Keep this simple and explicit so it is easy to mock in tests.
cred_manager = CredentialManager()
db_service = CosmosDBService(cred_manager)
task_repo = TaskRepository(db_service)
task_service = TaskService(task_repo)


def _json_response(payload, status_code=200):
    """Helper to build JSON responses consistently."""
    return func.HttpResponse(
        json.dumps(payload, ensure_ascii=False),
        status_code=status_code,
        mimetype="application/json"
    )


def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    Entry point for the Azure Function.
    Supports GET, POST and PATCH (partial updates).
    """
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

            if not title:
                return _json_response({"error": "Field 'title' is required"}, 400)
            if not user_id:
                # CosmosDBService.create_item currently requires user_id in the item
                return _json_response({"error": "Field 'user_id' is required"}, 400)

            # Build domain entity and persist (we add user_id to the dict because Cosmos expects it)
            task = Task(title=title)
            task_dict = task.to_dict()
            task_dict["user_id"] = user_id
            # Optionally store created_by / created_at metadata here (created_at already present)
            try:
                created = task_repo.create(task_dict)
                return _json_response(created, 201)
            except DatabaseError as e:
                logging.exception("Database error while creating task")
                return _json_response({"error": str(e)}, 500)

        elif req.method == "GET":
            # List tasks. If user_id query param provided, filter by user.
            user_id = req.params.get("user_id")
            try:
                if user_id:
                    query = "SELECT * FROM c WHERE c.type = @type AND c.user_id = @user_id"
                    params = [
                        {"name": "@type", "value": "task"},
                        {"name": "@user_id", "value": user_id}
                    ]
                    items = task_repo.query(query, params)
                else:
                    # Delegate to service which returns all tasks of type 'task'
                    items = task_service.list_tasks()
                return _json_response(items, 200)
            except DatabaseError as e:
                logging.exception("Database error while listing tasks")
                return _json_response({"error": str(e)}, 500)

        elif req.method == "PATCH":
            # Partial update — we use this to mark a task as completed.
            # Expect task id in route parameters: route: "tasks/{id?}"
            task_id = req.route_params.get("id") or req.params.get("id")
            if not task_id:
                return _json_response({"error": "Task id is required in route (tasks/{id})"}, 400)

            # Optional action body (defaults to complete)
            try:
                body = req.get_json() if req.get_body() else {}
            except ValueError:
                body = {}

            action = (body.get("action") or "complete").lower()

            if action == "complete":
                try:
                    updated = task_service.complete_task(task_id)
                    return _json_response(updated, 200)
                except DatabaseError as e:
                    # If not found, service/repo may raise DatabaseError - report 404 when appropriate
                    msg = str(e)
                    logging.exception(f"Error completing task {task_id}")
                    if "not found" in msg.lower():
                        return _json_response({"error": msg}, 404)
                    return _json_response({"error": msg}, 500)
            else:
                return _json_response({"error": f"Unsupported action '{action}'"}, 400)

        else:
            return _json_response({"error": f"Method {req.method} not allowed"}, 405)

    except Exception as e:
        logging.exception("Unexpected error in tasks function")
        return _json_response({"error": "Internal server error", "detail": str(e)}, 500)
