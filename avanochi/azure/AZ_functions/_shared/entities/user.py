# shared/entities/user.py
from datetime import datetime
import uuid


class User:
    # Domain entity representing a system user

    def __init__(self, name: str):
        self.id = str(uuid.uuid4())
        self.name = name
        self.created_at = datetime.utcnow().isoformat()
        self.updated_at = None

    def to_dict(self):
        return self.__dict__
