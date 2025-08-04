from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from .models import Task


class TaskManager:
    """Manages tasks stored in a JSON file."""

    def __init__(self, storage_path: Path):
        self.storage_path = Path(storage_path)
        self.tasks: List[Task] = []
        self._load()

    def _load(self) -> None:
        if self.storage_path.exists():
            data = json.loads(self.storage_path.read_text())
            self.tasks = []
            for item in data:
                if item.get("due"):
                    item["due"] = datetime.fromisoformat(item["due"]).date()
                self.tasks.append(Task(**item))
        else:
            self.tasks = []

    def _save(self) -> None:
        data = [task.__dict__ for task in self.tasks]
        self.storage_path.write_text(json.dumps(data, default=str, indent=2))

    def add_task(self, title: str, list_name: str = "Reminders", due: Optional[str] = None) -> Task:
        task_id = max([t.id for t in self.tasks], default=0) + 1
        due_date = datetime.fromisoformat(due).date() if due else None
        task = Task(id=task_id, title=title, list_name=list_name, due=due_date)
        self.tasks.append(task)
        self._save()
        return task

    def list_tasks(self, list_name: Optional[str] = None) -> List[Task]:
        tasks = self.tasks
        if list_name:
            tasks = [t for t in tasks if t.list_name == list_name]
        return tasks

    def complete_task(self, task_id: int) -> bool:
        for task in self.tasks:
            if task.id == task_id:
                task.completed = True
                self._save()
                return True
        return False
