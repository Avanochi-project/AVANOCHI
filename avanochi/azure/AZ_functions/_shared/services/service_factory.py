# shared/services/service_factory.py

from _shared.credential_manager import CredentialManager
from _shared.database import CosmosDBService
from _shared.auth_manager import AuthManager

# Repositories
from _shared.repos.task_repo import TaskRepository
from _shared.repos.work_session_repo import WorkSessionRepository
from _shared.repos.stats_repo import StatsRepository
from _shared.repos.auth_repo import AuthRepository
from _shared.repos.user_repo import UserRepository

# Services
from _shared.services.task_service import TaskService
from _shared.services.stats_service import StatsService
from _shared.services.work_session_service import WorkSessionService
from _shared.services.auth_service import AuthenticationService
from _shared.services.user_service import UserService


class ServiceFactory:
    
    # Centralized factory to build and provide services with their required repositories.
    # This keeps the endpoint code clean and ensures that services do not touch infrastructure.

    def __init__(self):
        # Initialize shared infrastructure once
        cred_manager = CredentialManager()
        db_service = CosmosDBService(cred_manager)
        auth_manager = AuthManager()

        # Initialize repositories
        self._task_repo = TaskRepository(db_service)
        self._ws_repo = WorkSessionRepository(db_service)
        self._stats_repo = StatsRepository(db_service)
        self._user_repo = UserRepository(db_service)
        self._auth_repo = AuthRepository(self._user_repo, auth_manager)

    def get_task_service(self) -> TaskService:
        return TaskService(self._task_repo)

    def get_stats_service(self) -> StatsService:
        return StatsService(self._stats_repo, self._ws_repo, self._user_repo)

    def get_work_session_service(self) -> WorkSessionService:
        return WorkSessionService(self._ws_repo)
    
    def get_user_service(self) -> UserService:
        return UserService(self._user_repo)

    def get_auth_service(self) -> AuthenticationService:
        return AuthenticationService(self._auth_repo)
    
