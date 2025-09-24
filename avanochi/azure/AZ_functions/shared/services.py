# shared/services.py
from shared.repositories import TaskRepository, WorkSessionRepository

class TaskService:
    def __init__(self):
        self.repo = TaskRepository()

    def create_task(self, title: str):
        return self.repo.create_task(title)

    def list_tasks(self):
        return self.repo.list_tasks()

    def complete_task(self, task_id: str):
        return self.repo.complete_task(task_id)


class WorkSessionService:
    def __init__(self):
        self.repo = WorkSessionRepository()

    def start_session(self, user_id: str):
        return self.repo.start_session(user_id)

    def end_session(self, session_id: str):
        return self.repo.end_session(session_id)
