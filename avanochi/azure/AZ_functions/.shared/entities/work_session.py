# shared/entities/work_session.py
from datetime import datetime
import uuid


class WorkSession:
    # Domain entity representing a working session of a user

    def __init__(self, user_id: str, start_time: str = None):
        self.id = str(uuid.uuid4())
        self.user_id = user_id
        self.start_time = start_time or datetime.utcnow().isoformat()
        self.end_time = None
        self.duration = None

    def end_session(self):
        # Mark session as finished and calculate duration in hours
        self.end_time = datetime.utcnow().isoformat()
        start = datetime.fromisoformat(self.start_time)
        end = datetime.fromisoformat(self.end_time)
        self.duration = round((end - start).total_seconds() / 3600, 2)

    def to_dict(self):
        return self.__dict__
