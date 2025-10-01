from _shared.services.base_service import BaseService
from _shared.repos.stats_repo import StatsRepository
from _shared.repos.work_session_repo import WorkSessionRepository

class StatsService(BaseService):
    # Service layer for user productivity statistics.

    def __init__(self, stats_repo: StatsRepository = None, ws_repo: WorkSessionRepository = None):
        self.stats_repo = stats_repo
        self.ws_repo = ws_repo

    def get_entity_type(self) -> str:
        return "Stats"

    def get_user_stats(self, user_id: str) -> dict:
        if not user_id:
            raise ValueError("user_id is required")

        # Hours worked
        sessions = self.ws_repo.list_sessions(user_id)
        total_hours = sum(float(s["duration"]) for s in sessions if s.get("duration"))

        # Tasks completed
        tasks_completed = self.stats_repo.count_completed_tasks(user_id)

        return {
            "user_id": user_id,
            "hours_worked": round(total_hours, 2),
            "tasks_completed": tasks_completed
        }
