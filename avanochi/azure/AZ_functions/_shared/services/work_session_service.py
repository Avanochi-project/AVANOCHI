# shared/services/work_session_service.py

from _shared.services.base_service import BaseService
from _shared.repos.work_session_repo import WorkSessionRepository
from _shared.entities.work_session import WorkSession


class WorkSessionService(BaseService):
    # Service layer for WorkSession operations.

    def __init__(self, repo: WorkSessionRepository):
        self.repo = repo

    def get_entity_type(self) -> str:
        return self.repo.entity_type()

    def start_session(self, user_id: str):
        if not user_id:
            raise ValueError("User ID is required to start a session")
        session = WorkSession(user_id)
        return self.repo.start_session(session.to_dict())

    def end_session(self, session_id: str):
        return self.repo.end_session(session_id)

    def get_active_session(self, user_id: str):
        return self.repo.get_active_session(user_id)

    def list_sessions(self, user_id: str):
        return self.repo.list_sessions(user_id)
