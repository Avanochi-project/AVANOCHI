# repositories/base/base_repo.py

from abc import ABC, abstractmethod
from shared.database import CosmosDBService, DatabaseError


class BaseRepository(ABC):
    # Abstract base repository with generic CRUD operations

    def __init__(self, db_service: CosmosDBService):
        self._db = db_service

    @abstractmethod
    def entity_type(self) -> str:
        # Must be implemented by child class (e.g. "task", "work_session")
        pass

    def create(self, entity: dict) -> dict:
        entity["type"] = self.entity_type()
        return self._db.create_item(entity)

    def get(self, entity_id: str) -> dict:
        return self._db.read_item(entity_id, partition_key=entity_id)

    def update(self, entity: dict) -> dict:
        return self._db.upsert_item(entity)

    def delete(self, entity_id: str) -> None:
        self._db.delete_item(entity_id, partition_key=entity_id)

    def query(self, query: str, params: list = None) -> list[dict]:
        return self._db.send_query(query, params)

# ====================================
#   CosmosDB Implementations
# ====================================

class CosmosTaskRepository(ITaskRepository):
    def __init__(self, db_service: CosmosDBService, container_name: str = "Tasks"):
        self.container = db_service.get_container(container_name)

    def create_task(self, task: Task):
        self.container.create_item(task.to_dict())
        return task.to_dict()

    def list_tasks(self):
        return list(self.container.read_all_items())

    def complete_task(self, task_id: str):
        task = self.container.read_item(task_id, partition_key=task_id)
        task["completed"] = True
        self.container.upsert_item(task)
        return task


class CosmosWorkSessionRepository(IWorkSessionRepository):
    def __init__(self, db_service: CosmosDBService, container_name: str = "WorkSessions"):
        self.container = db_service.get_container(container_name)

    def start_session(self, session: WorkSession):
        self.container.create_item(session.to_dict())
        return session.to_dict()

    def end_session(self, session_id: str):
        session = self.container.read_item(session_id, partition_key=session_id)
        ws = WorkSession(user_id=session["user_id"], start_time=session["start_time"])
        ws.id = session_id
        ws.end_session()
        self.container.upsert_item(ws.to_dict())
        return ws.to_dict()
