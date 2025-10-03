# function_app.py
import azure.functions as func
from endpoints.work.work_sessions import main as work_sessions_main
from endpoints.work.tasks import main as tasks_main
from endpoints.work.stats import main as stats_main
from endpoints.work.auth import main as auth_main

app = func.FunctionApp()

@app.function_name(name="WorkSessions")
@app.route(route="work_sessions/{*route}", methods=["GET", "POST"])
def work_sessions(req: func.HttpRequest) -> func.HttpResponse:
    return work_sessions_main(req)

@app.function_name(name="Tasks")
@app.route(route="tasks", methods=["GET", "POST", "PATCH"])
def tasks(req: func.HttpRequest) -> func.HttpResponse:
    return tasks_main(req)

@app.function_name(name="Stats")
@app.route(route="stats", methods=["GET"])
def stats(req: func.HttpRequest) -> func.HttpResponse:
    return stats_main(req)

@app.function_name(name="Auth")
@app.route(route="auth/{action}", methods=["GET", "POST"])
def auth(req: func.HttpRequest) -> func.HttpResponse:
    return auth_main(req)