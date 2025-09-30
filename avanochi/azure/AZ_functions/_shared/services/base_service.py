# shared/services/base_service.py
from abc import ABC, abstractmethod


class BaseService(ABC):
    # Abstract base class for all services.

    @abstractmethod
    def get_entity_type(self) -> str:
        # Returns the entity type handled by the service.
        pass
