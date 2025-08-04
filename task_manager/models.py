from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Task:
    """Represents a single task entry."""
    id: int
    title: str
    list_name: str = "Reminders"
    due: Optional[date] = None
    completed: bool = False
