# shared/entities/task.py
from datetime import datetime
import uuid

class Task:
    # Domain entity representing a task in the system

    def __init__(self, title: str, completed: bool = False):
        self.id = str(uuid.uuid4())
        self.title = title
        self.completed = completed
        self.created_at = datetime.utcnow().isoformat()
        self.updated_at = None

    def to_dict(self):
        return self.__dict__
