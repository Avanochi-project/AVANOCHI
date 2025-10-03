import json
import logging
import azure.functions as func

from _shared.database import DatabaseError

def _json_response(payload, status_code=200):
    # Helper to build JSON responses consistently.
    return func.HttpResponse(
        json.dumps(payload, ensure_ascii=False),
        status_code=status_code,
        mimetype="application/json"
    )

# =========================================================
#                     Task Handlers
# =========================================================

def create_task(req: func.HttpRequest, auth_service, task_service) -> func.HttpResponse:
    # Create a new task
    try:
        data = req.get_json()
    except ValueError:
        return _json_response({"error": "Invalid JSON payload"}, 400)

    title = (data.get("title") or "").strip()
    duration = data.get("duration")
    user_id = auth_service.validate_token(req)

    try:

        # MAIN ACTION
        created = task_service.create_task(user_id, title, duration)
        # SUCCESS

        return _json_response(
        {
            "task_id": created["id"]
        }
        , 201)
    except ValueError as ve:
        return _json_response({"error": str(ve)}, 400)
    except DatabaseError as e:
        logging.exception("Database error while creating task")
        return _json_response({"error": str(e)}, 500)

def list_tasks(req: func.HttpRequest, auth_service, task_service):
    user_id = auth_service.validate_token(req)
    try:

        # MAIN ACTION
        items = task_service.list_tasks(user_id)
        # SUCCESS

        return _json_response({"tasks": items}, 200)
    except DatabaseError as e:
        logging.exception("Database error while listing tasks")
        return _json_response({"error": str(e)}, 500)
    
def update_task_title(req: func.HttpRequest, auth_service, task_service):
    try:
        body = req.get_json()
    except ValueError:
        return _json_response({"error": "Invalid JSON body"}, 400)

    task_id = body.get("task_id")
    new_title = body.get("title", "").strip()
    if not task_id or not new_title:
        return _json_response({"error": "task_id and title are required"}, 400)

    try:
        
        # MAIN ACTION
        updated = task_service.update_task_title(task_id, new_title)
        # SUCCESS

        return _json_response({
            "task_id": updated["id"],
            "task_title": updated["title"]
        }, 200)
    except DatabaseError as e:
        msg = str(e)
        logging.exception(f"Error updating task title {task_id}")
        if "not found" in msg.lower():
            return _json_response({"error": msg}, 404)
        return _json_response({"error": msg}, 500)
    
def complete_task(req: func.HttpRequest, auth_service, task_service):
    try:
        body = req.get_json()
    except ValueError:
        return _json_response({"error": "Invalid JSON body"}, 400)

    task_id = body.get("task_id")
    if not task_id:
        return _json_response({"error": "Task id is required in body"}, 400)

    try:
        
        # MAIN ACTION
        updated = task_service.complete_task(task_id)
        # SUCCESS

        return _json_response({
            "task_id": updated["id"],
            "task_title": updated["title"],
            "completed": updated["completed"]
        }, 200)
    except DatabaseError as e:
        msg = str(e)
        logging.exception(f"Error completing task {task_id}")
        if "not found" in msg.lower():
            return _json_response({"error": msg}, 404)
        return _json_response({"error": msg}, 500)
