# _shared/repos/auth_repo.py
from _shared.repos.user_repo import UserRepository
from _shared.auth_manager import AuthManager
import hashlib

class AuthRepository:
    def __init__(self, user_repo: UserRepository, auth_manager: AuthManager):
        self.user_repo = user_repo
        self.auth_manager = auth_manager

    def hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def validate_user_credentials(self, username: str, password: str) -> dict | None:
        user = self.user_repo.find_by_name(username)
        if not user:
            return None
        if user.get("password_hash") != self.hash_password(password):
            return None
        return user

    def generate_token(self, user_id: str) -> str:
        return self.auth_manager.generate_token(user_id)

    def verify_token(self, token: str) -> dict:
        return self.auth_manager.verify_token(token)
