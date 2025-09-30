# repos/base_repo.py

from abc import ABC, abstractmethod
from _shared.database import CosmosDBService, DatabaseError


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
