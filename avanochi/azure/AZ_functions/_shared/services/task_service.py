# shared/services/task_service.py

from _shared.services.base_service import BaseService
from _shared.repos.task_repo import TaskRepository
from _shared.entities.task import Task, Subtask
from _shared.database import CosmosDBService
from _shared.credential_manager import CredentialManager

class TaskService(BaseService):
    # Service layer for Task operations.

    def __init__(self, task_repo: TaskRepository = None):
        self.repo = task_repo

    def get_entity_type(self) -> str:
        return "Task"

    # =========================================================
    #                   Task Operations
    # =========================================================

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
    
    def update_task_title(self, task_id: str, new_title: str) -> dict:
        if not task_id:
            raise ValueError("task_id is required")
        if not new_title or new_title.strip() == "":
            raise ValueError("New title cannot be empty")

        task = self.repo.get(task_id)
        if not task:
            raise ValueError("Task not found")

        task["title"] = new_title
        return self.repo.update(task)

    def complete_task(self, task_id: str) -> dict:
        return self.repo.complete_task(task_id)

    # =========================================================
    #                   SubTask Operations
    # =========================================================

    def add_subtask(self, task_id: str, title: str, index) -> dict:
        if not task_id:
            raise ValueError("task_id is required")
        if not title or title.strip() == "":
            raise ValueError("Subtask title cannot be empty")

        task = self.repo.get(task_id)
        if not task:
            raise ValueError("Task not found")

        subtask = Subtask(title, index)
        response = self.repo.add_subtask(task, subtask)

        return response
    
    def complete_subtask(self, task_id: str, subtask_id: str) -> dict:
        if not task_id:
            raise ValueError("task_id is required")
        if not subtask_id:
            raise ValueError("subtask_id is required")

        task = self.repo.get(task_id)
        subtasks = self.repo.get_subtasks(task_id, subtask_id)

        for subtask in subtasks:
            if subtask["id"] == subtask_id:
                subtask["completed"] = True
                break

        task["subtasks"] = subtasks
        response = self.repo.update(task)

        return response
    
    def delete_subtask(self, task_id: str, subtask_id: str) -> dict:
        if not task_id:
            raise ValueError("task_id is required")
        if not subtask_id:
            raise ValueError("subtask_id is required")

        task = self.repo.get(task_id)
        if not task:
            raise ValueError("Task not found")

        subtasks = task.get("subtasks", [])
        subtasks = [st for st in subtasks if st["id"] != subtask_id]
        task["subtasks"] = subtasks

        response = self.repo.update(task)
        return response