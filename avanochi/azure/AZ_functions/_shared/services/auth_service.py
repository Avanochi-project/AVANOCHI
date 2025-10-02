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
    
    def get_user_by_id(self, user_id: str) -> dict | None:
        return self.repo.get_user_by_id(user_id)

    def validate_token(self, req) -> bool:
        try:
            # Try with cookies
            cookie_result = {}
            try:
                cookie_result = self.repo.check_cookie_token(req.cookies)
            except Exception:
                cookie_result = {"valid": False}

            if cookie_result.get("valid"):
                return cookie_result.get("user_id")

            # Try with headers
            header_result = {}
            try:
                header_result = self.repo.check_header_token(req.headers)
            except Exception:
                header_result = {"valid": False}

            if header_result.get("valid"):
                return header_result.get("user_id")

            # If neither worked, return False
            return False

        except Exception as e:
            # Log the error si es necesario
            print(f"Token validation error: {e}")
            return False



