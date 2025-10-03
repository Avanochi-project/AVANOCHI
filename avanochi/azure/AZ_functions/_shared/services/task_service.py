# shared/services/task_service.py

from _shared.services.base_service import BaseService
from _shared.repos.task_repo import TaskRepository
from _shared.entities.task import Task
from _shared.database import CosmosDBService
from _shared.credential_manager import CredentialManager

class TaskService(BaseService):
    # Service layer for Task operations.

    def __init__(self, task_repo: TaskRepository = None):
        self.repo = task_repo

    def get_entity_type(self) -> str:
        return "Task"

    def create_task(self, user_id: str, title: str, duration) -> dict:
        if not title or title.strip() == "":
            raise ValueError("Task title cannot be empty")
        if not user_id:
            raise ValueError("Task must be associated to a user_id")

        task = Task(title)
        task_dict = task.to_dict()
        task_dict["user_id"] = user_id
        task_dict["duration"] = duration
        return self.repo.create_task(task_dict)

    def list_tasks(self, user_id: str = None) -> list:
        if user_id:
            return self.repo.list_tasks_by_user(user_id)
        return self.repo.list_tasks()

    def complete_task(self, task_id: str) -> dict:
        return self.repo.complete_task(task_id)
