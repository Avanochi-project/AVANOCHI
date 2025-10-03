# work/tasks/__init__.py

from .tasks import create_task, list_tasks, update_task_title, complete_task
from .subtasks import add_subtask, complete_subtask, delete_subtask


"""
HTTP-triggered Azure Function for basic task management (Phase 1).
Provides:

    IDs ARE GIVEN AS PARAMS OR IN BODY (JSON), NEVER IN URL PATH.

    - POST /tasks                      -> create a new task (requires title + user_id)
    - GET  /tasks                      -> list tasks (optional ?user_id=...)
    - PATCH /tasks/update_title        -> update a task's title
    - PATCH /tasks                     -> partial update (used to mark as completed)

    - POST /tasks/subtask/add          -> add a subtask to a task (requires title)
    - PATCH /tasks/subtask/complete    -> mark a subtask as completed
    - PATCH /tasks/subtask/delete      -> delete a subtask from a task

"""

import json
import azure.functions as func

from _shared.services.service_factory import ServiceFactory

# Initialize service once (through the factory)
factory = ServiceFactory()
task_service = factory.get_task_service()
auth_service = factory.get_auth_service()

def _json_response(payload, status_code=200):
    # Helper to build JSON responses consistently.
    return func.HttpResponse(
        json.dumps(payload, ensure_ascii=False),
        status_code=status_code,
        mimetype="application/json"
    )

def main(req: func.HttpRequest) -> func.HttpResponse:
    path = req.route_params.get("path") or req.params.get("path") or ""
    method = req.method.upper()

    if "subtask" in path:
        # dispatch subtask endpoints
        if method == "POST" and "add" in path:
            return add_subtask(req, auth_service, task_service)
        elif method == "PATCH" and "complete" in path:
            return complete_subtask(req, auth_service, task_service)
        elif method == "PATCH" and "delete" in path:
            return delete_subtask(req, auth_service, task_service)
        else:
            return _json_response({"error": "Subtask endpoint not found"}, 404)
    else:
        # dispatch task endpoints
        if method == "POST":
            return create_task(req, auth_service, task_service)
        elif method == "GET":
            return list_tasks(req, auth_service, task_service)
        elif method == "PATCH":
            if "update_title" in path:
                return update_task_title(req, auth_service, task_service)
            else:
                return complete_task(req, auth_service, task_service)
        else:
            return _json_response({"error": f"Method {method} not allowed"}, 405)

