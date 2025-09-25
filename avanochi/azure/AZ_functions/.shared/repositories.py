# shared/repositories.py
from abc import ABC, abstractmethod
from shared.entities import Task, WorkSession
from shared.database import CosmosDBService

# ==============================
#   Repository Interfaces
# ==============================

class ITaskRepository(ABC):
    @abstractmethod
    def create_task(self, task: Task): pass

    @abstractmethod
    def list_tasks(self): pass

    @abstractmethod
    def complete_task(self, task_id: str): pass


class IWorkSessionRepository(ABC):
    @abstractmethod
    def start_session(self, session: WorkSession): pass

    @abstractmethod
    def end_session(self, session_id: str): pass


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
