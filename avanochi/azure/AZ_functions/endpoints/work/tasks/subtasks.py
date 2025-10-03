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
#                    SubTask Handlers
# =========================================================

def add_subtask(req: func.HttpRequest, auth_service, task_service) -> func.HttpResponse:
    # Add a subtask to a task.
    try:
        body = req.get_json()
    except ValueError:
        return _json_response({"error": "Invalid JSON body"}, 400)

    task_id = body.get("task_id")
    index = body.get("index")
    title = (body.get("title") or "").strip()

    if not task_id or not title:
        return _json_response({"error": "task_id and title are required"}, 400)

    try:
        
        # MAIN ACTION
        subtask = task_service.add_subtask(task_id, title, index)
        # SUCCESS

        return _json_response({"subtask_id": subtask["id"]}, 201)
    except DatabaseError as e:
        logging.exception(f"Error adding subtask to task {task_id}")
        return _json_response({"error": str(e)}, 500)


def complete_subtask(req: func.HttpRequest, auth_service, task_service) -> func.HttpResponse:
    # Mark a subtask as completed.
    try:
        body = req.get_json()
    except ValueError:
        return _json_response({"error": "Invalid JSON body"}, 400)

    task_id = body.get("task_id")
    subtask_id = body.get("subtask_id")
    if not subtask_id:
        return _json_response({"error": "subtask_id is required"}, 400)

    try:
                
        # MAIN ACTION
        updated = task_service.complete_subtask(task_id, subtask_id)
        # SUCCESS

        return _json_response({
            "subtask_id": updated["id"],
            "title": updated["title"],
            "completed": updated["completed"]
        }, 200)
    except DatabaseError as e:
        logging.exception(f"Error completing subtask {subtask_id}")
        return _json_response({"error": str(e)}, 500)


def delete_subtask(req: func.HttpRequest, auth_service, task_service) -> func.HttpResponse:
    # Delete a subtask from a task.
    try:
        body = req.get_json()
    except ValueError:
        return _json_response({"error": "Invalid JSON body"}, 400)

    subtask_id = body.get("subtask_id")
    if not subtask_id:
        return _json_response({"error": "subtask_id is required"}, 400)

    try:
                
        # MAIN ACTION
        task_service.delete_subtask(subtask_id)
        # SUCCESS

        return _json_response({"subtask_id": subtask_id, "deleted": True}, 200)
    except DatabaseError as e:
        logging.exception(f"Error deleting subtask {subtask_id}")
        return _json_response({"error": str(e)}, 500)