import argparse
from pathlib import Path

from .manager import TaskManager


def main() -> None:
    parser = argparse.ArgumentParser(description="Apple Reminders-style task manager")
    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", help="Task title")
    add_parser.add_argument("--list", dest="list_name", default="Reminders", help="List name")
    add_parser.add_argument("--due", dest="due", help="Due date in YYYY-MM-DD format")

    list_parser = subparsers.add_parser("list", help="List tasks")
    list_parser.add_argument("--list", dest="list_name", help="List name to filter")

    complete_parser = subparsers.add_parser("complete", help="Mark task as complete")
    complete_parser.add_argument("id", type=int, help="ID of task to complete")

    args = parser.parse_args()
    manager = TaskManager(Path("tasks.json"))

    if args.command == "add":
        task = manager.add_task(args.title, args.list_name, args.due)
        print(f"Added task {task.id}: {task.title}")
    elif args.command == "list":
        tasks = manager.list_tasks(args.list_name)
        for task in tasks:
            status = "\u2713" if task.completed else " "
            due = f" (due {task.due.isoformat()})" if task.due else ""
            print(f"[{status}] {task.id}: {task.title}{due} — {task.list_name}")
    elif args.command == "complete":
        if manager.complete_task(args.id):
            print(f"Completed task {args.id}")
        else:
            print(f"Task {args.id} not found")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
