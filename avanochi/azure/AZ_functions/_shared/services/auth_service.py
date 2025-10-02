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

    def get_id_from_request(self, req):  
        user_id = self.repo.get_id_from_token(req)
        if not user_id:
            raise ValueError("Invalid or expired token")
        return user_id

    def validate_token(self, req) -> bool:
        # First try with cookies
        cookie_result = self.repo.check_cookie_token(req.cookies)
        if cookie_result.get("valid"):
            return True

        # Then try with headers
        header_result = self.repo.check_header_token(req.headers)
        if header_result.get("valid"):
            return True

        # If neither worked, return False
        return False


