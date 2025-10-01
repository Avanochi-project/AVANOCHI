from _shared.repos.base_repo import BaseRepository
from _shared.database import DatabaseError

class StatsRepository(BaseRepository):
    # Repository for aggregated statistics queries (no single entity type).

    def entity_type(self) -> str:
        # Stats is not a real entity stored in Cosmos,
        # but we need to comply with BaseRepository contract.
        return "stats"

    def count_completed_tasks(self, user_id: str) -> int:
        query = """
            SELECT VALUE COUNT(1)
            FROM c
            WHERE c.type = @type
              AND c.user_id = @user_id
              AND c.completed = true
        """
        params = [
            {"name": "@type", "value": "task"},
            {"name": "@user_id", "value": user_id}
        ]
        try:
            result = self.query(query, params)
            return result[0] if result else 0
        except Exception as e:
            raise DatabaseError(f"Error counting completed tasks: {e}")
