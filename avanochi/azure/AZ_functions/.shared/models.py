# shared/models.py
from datetime import datetime
import uuid

class Task:
    def __init__(self, title: str, completed: bool = False):
        self.id = str(uuid.uuid4())
        self.title = title
        self.completed = completed
        self.created_at = datetime.utcnow().isoformat()
        self.updated_at = None

    def to_dict(self):
        return self.__dict__


class WorkSession:
    def __init__(self, user_id: str, start_time: str = None):
        self.id = str(uuid.uuid4())
        self.user_id = user_id
        self.start_time = start_time or datetime.utcnow().isoformat()
        self.end_time = None
        self.duration = None

    def end_session(self):
        self.end_time = datetime.utcnow().isoformat()
        # Duración en horas (float)
        start = datetime.fromisoformat(self.start_time)
        end = datetime.fromisoformat(self.end_time)
        self.duration = round((end - start).total_seconds() / 3600, 2)

    def to_dict(self):
        return self.__dict__
