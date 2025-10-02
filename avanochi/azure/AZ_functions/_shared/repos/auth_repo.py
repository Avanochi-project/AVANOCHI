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

    def get_user_by_id(self, user_id: str) -> dict | None:
        return self.user_repo.get_user(user_id)

    def get_id_from_token(self, token: str) -> dict | None:
        payload = self.auth_manager.verify_token(token)
        if not payload or "user_id" not in payload:
            return None
        user_id = payload["user_id"]
        return user_id

    def check_cookie_token(self, cookies: dict) -> dict:
        token = cookies.get("auth_token")
        if not token:
            return {"valid": False, "error": "No token in cookie"}
        return self.auth_manager.verify_token(token)
    
    def check_header_token(self, headers: dict) -> dict:
        auth_header = headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return {"valid": False, "error": "No Bearer token in Authorization header"}
        token = auth_header.split(" ", 1)[1]
        return self.auth_manager.verify_token(token)