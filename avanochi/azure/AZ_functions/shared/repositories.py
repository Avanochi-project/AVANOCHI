# shared/repositories.py
from shared.db import get_container
from shared.models import Task, WorkSession

class TaskRepository:
    def __init__(self):
        self.container = get_container("Tasks")

    def create_task(self, title: str):
        task = Task(title)
        self.container.create_item(task.to_dict())
        return task.to_dict()

    def list_tasks(self):
        return list(self.container.read_all_items())

    def complete_task(self, task_id: str):
        task = self.container.read_item(task_id, partition_key=task_id)
        task["completed"] = True
        self.container.upsert_item(task)
        return task


class WorkSessionRepository:
    def __init__(self):
        self.container = get_container("WorkSessions")

    def start_session(self, user_id: str):
        session = WorkSession(user_id)
        self.container.create_item(session.to_dict())
        return session.to_dict()

    def end_session(self, session_id: str):
        session = self.container.read_item(session_id, partition_key=session_id)
        ws = WorkSession(user_id=session["user_id"], start_time=session["start_time"])
        ws.id = session_id
        ws.end_session()
        self.container.upsert_item(ws.to_dict())
        return ws.to_dict()
