# endpoints/work/stats/__init__.py

"""
HTTP-triggered Azure Function for statistics (Phase 1).
Provides:
 - GET /stats/{user_id} -> hours worked + tasks completed
"""

import json
import logging
import azure.functions as func

from _shared.database import DatabaseError
from _shared.services.service_factory import ServiceFactory

# Initialize service once
factory = ServiceFactory()
stats_service = factory.get_stats_service()
auth_service = factory.get_auth_service()

def _json_response(payload, status_code=200):
    return func.HttpResponse(
        json.dumps(payload, ensure_ascii=False),
        status_code=status_code,
        mimetype="application/json"
    )

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info(f"Stats function invoked. Method={req.method}")

    # AUTHENTICATION
    if not auth_service.validate_token(req):
        return _json_response({"error": "Unauthorized"}, 401)

    if req.method != "GET":
        return _json_response({"error": f"Method {req.method} not allowed"}, 405)

    user_id = auth_service.get_id_from_request(req)

    try:
        stats = stats_service.get_user_stats(user_id)
        return _json_response(stats, 200)

    except DatabaseError as e:
        logging.exception("Database error while generating stats")
        return _json_response({"error": str(e)}, 500)
    except Exception as e:
        logging.exception("Unexpected error in stats function")
        return _json_response({"error": "Internal server error", "detail": str(e)}, 500)
