# shared/services/user_service.py
from _shared.services.base_service import BaseService
from _shared.repos.user_repository import UserRepository
from _shared.entities.user import User


class UserService(BaseService):
    # Service layer for User operations.

    def __init__(self, repo: UserRepository):
        self.repo = repo

    def get_entity_type(self) -> str:
        return "User"

    def create_user(self, name: str):
        if not name or name.strip() == "":
            raise ValueError("User name cannot be empty")
        user = User(name)
        return self.repo.create_user(user)

    def get_user(self, user_id: str):
        return self.repo.get_user(user_id)

    def update_user(self, user: User):
        return self.repo.update_user(user)

    def delete_user(self, user_id: str):
        return self.repo.delete_user(user_id)

    def list_users(self):
        return self.repo.list_users()
