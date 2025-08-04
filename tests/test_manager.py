from pathlib import Path

from task_manager.manager import TaskManager


def test_add_and_list(tmp_path: Path) -> None:
    storage = tmp_path / "tasks.json"
    manager = TaskManager(storage)
    manager.add_task("Buy milk", "Groceries")
    tasks = manager.list_tasks()
    assert len(tasks) == 1
    assert tasks[0].title == "Buy milk"
    assert tasks[0].list_name == "Groceries"


def test_complete_task(tmp_path: Path) -> None:
    storage = tmp_path / "tasks.json"
    manager = TaskManager(storage)
    task = manager.add_task("Read book")
    assert manager.complete_task(task.id) is True
    assert manager.list_tasks()[0].completed is True
