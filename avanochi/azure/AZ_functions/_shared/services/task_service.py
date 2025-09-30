# shared/services/task_service.py
from _shared.services.base_service import BaseService
from _shared.repos.task_repository import TaskRepository
from _shared.entities.task import Task


class TaskService(BaseService):
    # Service layer for Task operations.

    def __init__(self, repo: TaskRepository):
        self.repo = repo

    def get_entity_type(self) -> str:
        return "Task"

    def create_task(self, title: str):
        if not title or title.strip() == "":
            raise ValueError("Task title cannot be empty")
        task = Task(title)
        return self.repo.create_task(task)

    def list_tasks(self):
        return self.repo.list_tasks()

    def complete_task(self, task_id: str):
        return self.repo.complete_task(task_id)
