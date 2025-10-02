# _shared/services/authentication_service.py
from _shared.services.base_service import BaseService
from _shared.repos.auth_repo import AuthRepository

class AuthenticationService(BaseService):
    def __init__(self, repo: AuthRepository):
        self.repo = repo

    def get_entity_type(self) -> str:
        return "Auth"

    def register(self, username: str, password: str):
        # Check if user exists
        if self.repo.user_repo.find_by_name(username):
            raise ValueError("Username already exists")

        password_hash = self.repo.hash_password(password)
        user = {"name": username, "password_hash": password_hash}
        return self.repo.user_repo.create(user)

    def login(self, username: str, password: str) -> str:
        user = self.repo.validate_user_credentials(username, password)
        if not user:
            raise ValueError("Invalid username or password")
        return self.repo.generate_token(user["id"])

    def validate_token(self, token: str) -> bool:
        return (
            self.repo.check_cookie_token({"auth_token": token})["valid"] or
            self.repo.check_header_token({"Authorization": f"Bearer {token}"})["valid"]
        )

