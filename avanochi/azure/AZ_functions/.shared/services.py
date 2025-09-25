# shared/services.py
from shared.repositories import ITaskRepository, IWorkSessionRepository
from shared.models import Task, WorkSession

class TaskService:
    # Service layer for Task operations.
    
    def __init__(self, repo: ITaskRepository):
        self.repo = repo

    def create_task(self, title: str):
        task = Task(title)
        return self.repo.create_task(task)

    def list_tasks(self):
        return self.repo.list_tasks()

    def complete_task(self, task_id: str):
        return self.repo.complete_task(task_id)


class WorkSessionService:
    # Service layer for WorkSession operations.

    def __init__(self, repo: IWorkSessionRepository):
        self.repo = repo

    def start_session(self, user_id: str):
        session = WorkSession(user_id)
        return self.repo.start_session(session)

    def end_session(self, session_id: str):
        return self.repo.end_session(session_id)
