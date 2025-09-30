# shared/repos/task_repo.py

from _shared.repos.base_repo import BaseRepository
from _shared.entities import Task

class TaskRepository(BaseRepository):
    # Repository for managing Task entities in Cosmos DB

    def entity_type(self) -> str:
        return "task"

    def create_task(self, task: Task):
        return self.create(task.to_dict())

    def list_tasks(self):
        query = "SELECT * FROM c WHERE c.type = @type"
        params = [{"name": "@type", "value": self.entity_type()}]
        return self.query(query, params)

    def complete_task(self, task_id: str):
        task = self.get(task_id)
        task["completed"] = True
        return self.update(task)
