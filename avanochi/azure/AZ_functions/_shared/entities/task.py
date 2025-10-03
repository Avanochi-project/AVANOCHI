# shared/entities/task.py
from datetime import datetime
import uuid

class Task:
    # Domain entity representing a task in the system

    def __init__(self, title: str, status: bool = False):
        self.id = str(uuid.uuid4())
        self.title = title
        self.status = status
        self.duration = None
        self.created_at = datetime.utcnow().isoformat()
        self.due_date = None
        self.subtasks = []

    def to_dict(self):
        return self.__dict__

    def add_subtask(self, subtask):
        self.subtasks.append(subtask)

class Subtask:
    # Domain entity representing a subtask associated with a task

    def __init__(self, title: str, index, status: bool = False):
        self.id = str(uuid.uuid4())
        self.title = title
        self.index = index
        self.status = status

    def to_dict(self):
        return self.__dict__