# shared/repos/work_session_repository.py

from shared.repos.base_repo import BaseRepository
from shared.entities import WorkSession


class WorkSessionRepository(BaseRepository):
    # Repository for managing WorkSession entities in Cosmos DB

    def entity_type(self) -> str:
        return "work_session"

    def start_session(self, session: WorkSession):
        return self.create(session.to_dict())

    def end_session(self, session_id: str):
        session = self.get(session_id)
        ws = WorkSession(user_id=session["user_id"], start_time=session["start_time"])
        ws.id = session_id
        ws.end_session()
        return self.update(ws.to_dict())

    def get_active_session(self, user_id: str):
        query = "SELECT * FROM c WHERE c.type = @type AND c.user_id = @user_id AND IS_NULL(c.end_time)"
        params = [{"name": "@type", "value": self.entity_type()}, {"name": "@user_id", "value": user_id}]
        results = self.query(query, params)
        return results[0] if results else None

    def list_sessions(self, user_id: str):
        query = "SELECT * FROM c WHERE c.type = @type AND c.user_id = @user_id"
        params = [{"name": "@type", "value": self.entity_type()}, {"name": "@user_id", "value": user_id}]
        return self.query(query, params)
