# shared/repos/user_repo.py

from shared.repos.base_repo import BaseRepository
from shared.entities import User

class UserRepository(BaseRepository):
    # Repository for managing User entities in Cosmos DB

    def entity_type(self) -> str:
        return "user"

    def create_user(self, user: User):
        # Persist a new user in the database
        return self.create(user.to_dict())

    def get_user(self, user_id: str):
        # Retrieve a single user by ID
        return self.get(user_id)

    def update_user(self, user: User):
        # Update an existing user
        return self.update(user.to_dict())

    def delete_user(self, user_id: str):
        # Delete a user by ID
        return self.delete(user_id)

    def list_users(self):
        # List all users in the database
        query = "SELECT * FROM c WHERE c.type = @type"
        params = [{"name": "@type", "value": self.entity_type()}]
        return self.query(query, params)
