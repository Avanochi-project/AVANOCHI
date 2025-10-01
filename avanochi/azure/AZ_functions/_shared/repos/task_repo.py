# shared/repos/task_repo.py

from _shared.repos.base_repo import BaseRepository
from _shared.entities import Task

class TaskRepository(BaseRepository):
    # Repository for managing Task entities in Cosmos DB

    def entity_type(self) -> str:
        return "task"

    def create_task(self, task: Task | dict):
        # Accepts Task entity or dict
        if isinstance(task, Task):
            return self.create(task.to_dict())
        return self.create(task)

    def list_tasks(self):
        query = "SELECT * FROM c WHERE c.type = @type"
        params = [{"name": "@type", "value": self.entity_type()}]
        return self.query(query, params)

    def list_tasks_by_user(self, user_id: str):
        query = "SELECT * FROM c WHERE c.type = @type AND c.user_id = @user_id"
        params = [
            {"name": "@type", "value": self.entity_type()},
            {"name": "@user_id", "value": user_id}
        ]
        return self.query(query, params)

    def complete_task(self, task_id: str):
        task = self.get(task_id)
        task["completed"] = True
        return self.update(task)
