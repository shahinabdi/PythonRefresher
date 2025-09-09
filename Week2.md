# Week 2: Advanced Task Manager CLI

## 🎯 Project Overview

Build a professional-grade task management CLI tool that's actually useful for daily work. This isn't a toy project - it's something you'd put on your resume!

### ✨ Features
- ✅ Create, edit, delete tasks with priorities
- 📅 Due dates and automatic reminders
- 🏷️ Categories and tags
- 🔍 Advanced search and filtering
- 📊 Task statistics and productivity insights
- 📤 Export to CSV/JSON formats
- 🎨 Beautiful CLI interface with colors
- ⚡ Fast performance with proper data structures

---

## 🏗️ Project Structure

```
task-manager-cli/
├── src/
│   ├── __init__.py
│   ├── main.py              # CLI entry point
│   ├── models/
│   │   ├── __init__.py
│   │   ├── task.py          # Task class
│   │   └── task_manager.py  # TaskManager class
│   ├── services/
│   │   ├── __init__.py
│   │   ├── storage.py       # File I/O operations
│   │   ├── export.py        # Export functionality
│   │   └── analytics.py     # Task analytics
│   └── utils/
│       ├── __init__.py
│       ├── validators.py    # Input validation
│       └── formatters.py    # Output formatting
├── tests/
│   ├── test_task.py
│   ├── test_task_manager.py
│   └── test_storage.py
├── data/
│   └── .gitkeep
├── docker/
│   └── Dockerfile
├── .github/
│   └── workflows/
│       └── ci.yml
├── pyproject.toml
├── docker-compose.yml
├── README.md
└── .gitignore
```

---

## 🚀 Setup & Installation

### 1. Initialize Project
```bash
mkdir task-manager-cli
cd task-manager-cli
uv init
```

### 2. Configure pyproject.toml
```toml
[project]
name = "task-manager-cli"
version = "0.1.0"
description = "Professional task management CLI tool"
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    "click>=8.1.7",
    "rich>=13.7.0",
    "typer>=0.9.0",
    "pydantic>=2.5.0",
    "python-dateutil>=2.8.2",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "black>=23.0.0",
    "ruff>=0.1.0",
    "mypy>=1.8.0",
]

[project.scripts]
task = "src.main:app"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.ruff]
line-length = 88
target-version = "py311"
select = ["E", "F", "I", "N", "UP"]

[tool.black]
line-length = 88
target-version = ["py311"]

[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
```

### 3. Install Dependencies
```bash
uv sync --all-extras
```

---

## 💻 Core Implementation

### Task Model (src/models/task.py)
```python
from datetime import datetime, date
from enum import Enum
from typing import Optional, List, Set
from pydantic import BaseModel, Field
import uuid

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class Status(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    CANCELLED = "cancelled"

class Task(BaseModel):
    """
    Professional Task model with validation and rich features
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = None
    priority: Priority = Priority.MEDIUM
    status: Status = Status.TODO
    category: Optional[str] = None
    tags: Set[str] = Field(default_factory=set)
    due_date: Optional[date] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    
    def __str__(self) -> str:
        return f"Task({self.title}, {self.priority.value}, {self.status.value})"
    
    def is_overdue(self) -> bool:
        """Check if task is overdue"""
        if not self.due_date or self.status in [Status.DONE, Status.CANCELLED]:
            return False
        return date.today() > self.due_date
    
    def days_until_due(self) -> Optional[int]:
        """Get days until due date (negative if overdue)"""
        if not self.due_date:
            return None
        return (self.due_date - date.today()).days
    
    def mark_completed(self):
        """Mark task as completed"""
        self.status = Status.DONE
        self.completed_at = datetime.now()
        self.updated_at = datetime.now()
    
    def add_tag(self, tag: str):
        """Add a tag to the task"""
        self.tags.add(tag.lower().strip())
        self.updated_at = datetime.now()
    
    def remove_tag(self, tag: str):
        """Remove a tag from the task"""
        self.tags.discard(tag.lower().strip())
        self.updated_at = datetime.now()
```

### Task Manager (src/models/task_manager.py)
```python
from typing import List, Optional, Dict, Set
from datetime import date, datetime
from .task import Task, Priority, Status
from ..services.storage import StorageService

class TaskManager:
    """
    Main task management logic with efficient operations
    """
    
    def __init__(self, storage_service: StorageService):
        self.storage = storage_service
        self._tasks: Dict[str, Task] = {}
        self.load_tasks()
    
    def load_tasks(self):
        """Load tasks from storage"""
        self._tasks = {task.id: task for task in self.storage.load_all()}
    
    def save_tasks(self):
        """Save all tasks to storage"""
        self.storage.save_all(list(self._tasks.values()))
    
    def create_task(
        self,
        title: str,
        description: Optional[str] = None,
        priority: Priority = Priority.MEDIUM,
        category: Optional[str] = None,
        due_date: Optional[date] = None,
        tags: Optional[List[str]] = None
    ) -> Task:
        """Create a new task"""
        task = Task(
            title=title,
            description=description,
            priority=priority,
            category=category,
            due_date=due_date,
            tags=set(tags or [])
        )
        self._tasks[task.id] = task
        self.save_tasks()
        return task
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """Get task by ID"""
        return self._tasks.get(task_id)
    
    def update_task(self, task_id: str, **updates) -> Optional[Task]:
        """Update task with new values"""
        task = self._tasks.get(task_id)
        if not task:
            return None
        
        for field, value in updates.items():
            if hasattr(task, field):
                setattr(task, field, value)
        
        task.updated_at = datetime.now()
        self.save_tasks()
        return task
    
    def delete_task(self, task_id: str) -> bool:
        """Delete task by ID"""
        if task_id in self._tasks:
            del self._tasks[task_id]
            self.save_tasks()
            return True
        return False
    
    def get_all_tasks(self) -> List[Task]:
        """Get all tasks"""
        return list(self._tasks.values())
    
    def get_tasks_by_status(self, status: Status) -> List[Task]:
        """Get tasks by status"""
        return [task for task in self._tasks.values() if task.status == status]
    
    def get_tasks_by_priority(self, priority: Priority) -> List[Task]:
        """Get tasks by priority"""
        return [task for task in self._tasks.values() if task.priority == priority]
    
    def get_tasks_by_category(self, category: str) -> List[Task]:
        """Get tasks by category"""
        return [task for task in self._tasks.values() 
                if task.category and task.category.lower() == category.lower()]
    
    def get_overdue_tasks(self) -> List[Task]:
        """Get all overdue tasks"""
        return [task for task in self._tasks.values() if task.is_overdue()]
    
    def search_tasks(self, query: str) -> List[Task]:
        """Search tasks by title or description"""
        query = query.lower()
        results = []
        for task in self._tasks.values():
            if (query in task.title.lower() or 
                (task.description and query in task.description.lower()) or
                query in [tag.lower() for tag in task.tags]):
                results.append(task)
        return results
    
    def get_all_categories(self) -> Set[str]:
        """Get all unique categories"""
        return {task.category for task in self._tasks.values() 
                if task.category}
    
    def get_all_tags(self) -> Set[str]:
        """Get all unique tags"""
        all_tags = set()
        for task in self._tasks.values():
            all_tags.update(task.tags)
        return all_tags
    
    def get_task_count_by_status(self) -> Dict[Status, int]:
        """Get count of tasks by status"""
        counts = {status: 0 for status in Status}
        for task in self._tasks.values():
            counts[task.status] += 1
        return counts
```

### Storage Service (src/services/storage.py)
```python
import json
import os
from typing import List, Dict, Any
from datetime import datetime, date
from pathlib import Path
from ..models.task import Task

class StorageService:
    """
    Handle file I/O operations with proper error handling
    """
    
    def __init__(self, file_path: str = "data/tasks.json"):
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
    
    def load_all(self) -> List[Task]:
        """Load all tasks from file"""
        if not self.file_path.exists():
            return []
        
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [self._dict_to_task(task_dict) for task_dict in data]
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            print(f"Warning: Could not load tasks file: {e}")
            return []
    
    def save_all(self, tasks: List[Task]):
        """Save all tasks to file"""
        try:
            task_dicts = [self._task_to_dict(task) for task in tasks]
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(task_dicts, f, indent=2, ensure_ascii=False)
        except (OSError, ValueError) as e:
            print(f"Error: Could not save tasks: {e}")
    
    def _task_to_dict(self, task: Task) -> Dict[str, Any]:
        """Convert Task to dictionary for JSON serialization"""
        data = task.model_dump()
        # Convert dates and datetimes to ISO strings
        if data['due_date']:
            data['due_date'] = data['due_date'].isoformat()
        data['created_at'] = data['created_at'].isoformat()
        data['updated_at'] = data['updated_at'].isoformat()
        if data['completed_at']:
            data['completed_at'] = data['completed_at'].isoformat()
        # Convert set to list for JSON
        data['tags'] = list(data['tags'])
        return data
    
    def _dict_to_task(self, data: Dict[str, Any]) -> Task:
        """Convert dictionary to Task object"""
        # Convert ISO strings back to dates/datetimes
        if data['due_date']:
            data['due_date'] = date.fromisoformat(data['due_date'])
        data['created_at'] = datetime.fromisoformat(data['created_at'])
        data['updated_at'] = datetime.fromisoformat(data['updated_at'])
        if data['completed_at']:
            data['completed_at'] = datetime.fromisoformat(data['completed_at'])
        # Convert list back to set
        data['tags'] = set(data['tags'])
        return Task(**data)
```

### CLI Interface (src/main.py)
```python
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.text import Text
from datetime import date, datetime
from typing import Optional, List
from .models.task import Task, Priority, Status
from .models.task_manager import TaskManager
from .services.storage import StorageService
from .services.export import ExportService
from .services.analytics import AnalyticsService

app = typer.Typer(help="Professional Task Manager CLI")
console = Console()

# Initialize services
storage_service = StorageService()
task_manager = TaskManager(storage_service)
export_service = ExportService()
analytics_service = AnalyticsService()

@app.command("add")
def add_task(
    title: str = typer.Argument(..., help="Task title"),
    description: Optional[str] = typer.Option(None, "--desc", "-d", help="Task description"),
    priority: Priority = typer.Option(Priority.MEDIUM, "--priority", "-p", help="Task priority"),
    category: Optional[str] = typer.Option(None, "--category", "-c", help="Task category"),
    due: Optional[str] = typer.Option(None, "--due", help="Due date (YYYY-MM-DD)"),
    tags: Optional[List[str]] = typer.Option(None, "--tag", "-t", help="Tags (can be used multiple times)")
):
    """Add a new task"""
    due_date = None
    if due:
        try:
            due_date = datetime.strptime(due, "%Y-%m-%d").date()
        except ValueError:
            console.print("[red]Error: Invalid date format. Use YYYY-MM-DD[/red]")
            return
    
    task = task_manager.create_task(
        title=title,
        description=description,
        priority=priority,
        category=category,
        due_date=due_date,
        tags=tags or []
    )
    
    console.print(f"[green]✅ Task created:[/green] {task.title}")

@app.command("list")
def list_tasks(
    status: Optional[Status] = typer.Option(None, "--status", "-s", help="Filter by status"),
    category: Optional[str] = typer.Option(None, "--category", "-c", help="Filter by category"),
    priority: Optional[Priority] = typer.Option(None, "--priority", "-p", help="Filter by priority"),
    overdue: bool = typer.Option(False, "--overdue", help="Show only overdue tasks")
):
    """List tasks with optional filtering"""
    if overdue:
        tasks = task_manager.get_overdue_tasks()
    elif status:
        tasks = task_manager.get_tasks_by_status(status)
    elif category:
        tasks = task_manager.get_tasks_by_category(category)
    elif priority:
        tasks = task_manager.get_tasks_by_priority(priority)
    else:
        tasks = task_manager.get_all_tasks()
    
    if not tasks:
        console.print("[yellow]No tasks found[/yellow]")
        return
    
    _display_tasks_table(tasks)

@app.command("complete")
def complete_task(task_id: str = typer.Argument(..., help="Task ID")):
    """Mark task as completed"""
    task = task_manager.get_task(task_id)
    if not task:
        console.print("[red]Task not found[/red]")
        return
    
    task.mark_completed()
    task_manager.save_tasks()
    console.print(f"[green]✅ Task completed:[/green] {task.title}")

@app.command("delete")
def delete_task(task_id: str = typer.Argument(..., help="Task ID")):
    """Delete a task"""
    task = task_manager.get_task(task_id)
    if not task:
        console.print("[red]Task not found[/red]")
        return
    
    if Confirm.ask(f"Delete task '{task.title}'?"):
        task_manager.delete_task(task_id)
        console.print("[green]Task deleted[/green]")

@app.command("search")
def search_tasks(query: str = typer.Argument(..., help="Search query")):
    """Search tasks by title, description, or tags"""
    tasks = task_manager.search_tasks(query)
    if not tasks:
        console.print(f"[yellow]No tasks found for '{query}'[/yellow]")
        return
    
    console.print(f"[blue]Search results for '{query}':[/blue]")
    _display_tasks_table(tasks)

@app.command("stats")
def show_statistics():
    """Show task statistics and analytics"""
    stats = analytics_service.get_task_statistics(task_manager)
    
    # Create a fancy statistics display
    table = Table(title="📊 Task Statistics")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    
    for metric, value in stats.items():
        table.add_row(metric.replace('_', ' ').title(), str(value))
    
    console.print(table)

@app.command("export")
def export_tasks(
    format: str = typer.Option("json", help="Export format (json/csv)"),
    output: str = typer.Option("tasks", help="Output file name (without extension)")
):
    """Export tasks to JSON or CSV"""
    tasks = task_manager.get_all_tasks()
    
    if format.lower() == "csv":
        filename = export_service.export_to_csv(tasks, f"{output}.csv")
    else:
        filename = export_service.export_to_json(tasks, f"{output}.json")
    
    console.print(f"[green]Tasks exported to {filename}[/green]")

def _display_tasks_table(tasks: List[Task]):
    """Display tasks in a beautiful table"""
    table = Table(title="📋 Tasks")
    table.add_column("ID", style="dim")
    table.add_column("Title")
    table.add_column("Priority", justify="center")
    table.add_column("Status", justify="center")
    table.add_column("Category", style="cyan")
    table.add_column("Due Date", style="yellow")
    table.add_column("Tags", style="magenta")
    
    for task in sorted(tasks, key=lambda t: t.created_at, reverse=True):
        # Color-code priority
        priority_colors = {
            Priority.LOW: "green",
            Priority.MEDIUM: "yellow", 
            Priority.HIGH: "orange",
            Priority.URGENT: "red"
        }
        
        # Color-code status
        status_colors = {
            Status.TODO: "yellow",
            Status.IN_PROGRESS: "blue",
            Status.DONE: "green",
            Status.CANCELLED: "red"
        }
        
        due_str = task.due_date.strftime("%Y-%m-%d") if task.due_date else ""
        if task.is_overdue():
            due_str = f"[red]{due_str} (OVERDUE)[/red]"
        
        table.add_row(
            task.id[:8],  # Short ID
            task.title,
            f"[{priority_colors[task.priority]}]{task.priority.value}[/{priority_colors[task.priority]}]",
            f"[{status_colors[task.status]}]{task.status.value.replace('_', ' ')}[/{status_colors[task.status]}]",
            task.category or "",
            due_str,
            ", ".join(task.tags)
        )
    
    console.print(table)

if __name__ == "__main__":
    app()
```

---

## 🧪 Testing Suite

### Test Task Model (tests/test_task.py)
```python
import pytest
from datetime import date, datetime, timedelta
from src.models.task import Task, Priority, Status

def test_task_creation():
    """Test basic task creation"""
    task = Task(title="Test Task", priority=Priority.HIGH)
    
    assert task.title == "Test Task"
    assert task.priority == Priority.HIGH
    assert task.status == Status.TODO
    assert isinstance(task.created_at, datetime)

def test_task_is_overdue():
    """Test overdue detection"""
    # Task due yesterday
    overdue_task = Task(
        title="Overdue",
        due_date=date.today() - timedelta(days=1)
    )
    assert overdue_task.is_overdue()
    
    # Task due tomorrow
    future_task = Task(
        title="Future",
        due_date=date.today() + timedelta(days=1)
    )
    assert not future_task.is_overdue()
    
    # Completed overdue task
    completed_task = Task(
        title="Done",
        due_date=date.today() - timedelta(days=1),
        status=Status.DONE
    )
    assert not completed_task.is_overdue()

def test_task_completion():
    """Test task completion functionality"""
    task = Task(title="Complete me")
    assert task.status == Status.TODO
    assert task.completed_at is None
    
    task.mark_completed()
    assert task.status == Status.DONE
    assert task.completed_at is not None
    assert isinstance(task.completed_at, datetime)

def test_task_tags():
    """Test tag management"""
    task = Task(title="Tagged task")
    
    # Add tags
    task.add_tag("urgent")
    task.add_tag("WORK")  # Should be normalized
    assert "urgent" in task.tags
    assert "work" in task.tags
    
    # Remove tag
    task.remove_tag("urgent")
    assert "urgent" not in task.tags
    assert "work" in task.tags

def test_days_until_due():
    """Test due date calculations"""
    # Task due in 3 days
    future_task = Task(
        title="Future",
        due_date=date.today() + timedelta(days=3)
    )
    assert future_task.days_until_due() == 3
    
    # Overdue task
    overdue_task = Task(
        title="Overdue",
        due_date=date.today() - timedelta(days=2)
    )
    assert overdue_task.days_until_due() == -2
    
    # No due date
    no_due_task = Task(title="No due date")
    assert no_due_task.days_until_due() is None
```

### Test Task Manager (tests/test_task_manager.py)
```python
import pytest
import tempfile
import os
from datetime import date, timedelta
from src.models.task import Task, Priority, Status
from src.models.task_manager import TaskManager
from src.services.storage import StorageService

@pytest.fixture
def temp_storage():
    """Create temporary storage for testing"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_file = f.name
    
    storage = StorageService(temp_file)
    yield storage
    
    # Cleanup
    if os.path.exists(temp_file):
        os.unlink(temp_file)

@pytest.fixture
def task_manager(temp_storage):
    """Create task manager with temp storage"""
    return TaskManager(temp_storage)

def test_create_task(task_manager):
    """Test task creation"""
    task = task_manager.create_task(
        title="Test Task",
        priority=Priority.HIGH,
        category="Work"
    )
    
    assert task.title == "Test Task"
    assert task.priority == Priority.HIGH
    assert task.category == "Work"
    assert len(task_manager.get_all_tasks()) == 1

def test_get_task(task_manager):
    """Test task retrieval"""
    task = task_manager.create_task("Test Task")
    retrieved = task_manager.get_task(task.id)
    
    assert retrieved is not None
    assert retrieved.id == task.id
    assert retrieved.title == task.title

def test_update_task(task_manager):
    """Test task updates"""
    task = task_manager.create_task("Original Title")
    
    updated = task_manager.update_task(
        task.id,
        title="Updated Title",
        priority=Priority.URGENT
    )
    
    assert updated is not None
    assert updated.title == "Updated Title"
    assert updated.priority == Priority.URGENT

def test_delete_task(task_manager):
    """Test task deletion"""
    task = task_manager.create_task("Delete me")
    assert len(task_manager.get_all_tasks()) == 1
    
    deleted = task_manager.delete_task(task.id)
    assert deleted is True
    assert len(task_manager.get_all_tasks()) == 0

def test_filter_by_status(task_manager):
    """Test filtering tasks by status"""
    task1 = task_manager.create_task("Todo Task")
    task2 = task_manager.create_task("In Progress Task")
    task_manager.update_task(task2.id, status=Status.IN_PROGRESS)
    
    todo_tasks = task_manager.get_tasks_by_status(Status.TODO)
    in_progress_tasks = task_manager.get_tasks_by_status(Status.IN_PROGRESS)
    
    assert len(todo_tasks) == 1
    assert len(in_progress_tasks) == 1
    assert todo_tasks[0].id == task1.id

def test_search_tasks(task_manager):
    """Test task search functionality"""
    task1 = task_manager.create_task("Python Development", description="Learn FastAPI")
    task2 = task_manager.create_task("Go Shopping", description="Buy groceries")
    task3 = task_manager.create_task("Study Algorithms")
    task3.add_tag("python")
    task_manager.update_task(task3.id, tags=task3.tags)
    
    # Search in title
    python_tasks = task_manager.search_tasks("Python")
    assert len(python_tasks) == 1
    assert python_tasks[0].id == task1.id
    
    # Search in description
    api_tasks = task_manager.search_tasks("FastAPI")
    assert len(api_tasks) == 1
    
    # Search in tags
    tag_tasks = task_manager.search_tasks("python")
    assert len(tag_tasks) == 1  # Should find the tagged task

def test_overdue_tasks(task_manager):
    """Test overdue task detection"""
    # Create overdue task
    overdue = task_manager.create_task(
        "Overdue Task",
        due_date=date.today() - timedelta(days=1)
    )
    
    # Create future task
    future = task_manager.create_task(
        "Future Task",
        due_date=date.today() + timedelta(days=1)
    )
    
    overdue_tasks = task_manager.get_overdue_tasks()
    assert len(overdue_tasks) == 1
    assert overdue_tasks[0].id == overdue.id

def test_categories_and_tags(task_manager):
    """Test category and tag aggregation"""
    task1 = task_manager.create_task("Work Task", category="Work")
    task2 = task_manager.create_task("Personal Task", category="Personal")
    
    task1.add_tag("urgent")
    task1.add_tag("backend")
    task2.add_tag("shopping")
    
    task_manager.update_task(task1.id, tags=task1.tags)
    task_manager.update_task(task2.id, tags=task2.tags)
    
    categories = task_manager.get_all_categories()
    tags = task_manager.get_all_tags()
    
    assert "Work" in categories
    assert "Personal" in categories
    assert "urgent" in tags
    assert "backend" in tags
    assert "shopping" in tags
```

---

## 🛠️ Additional Services

### Export Service (src/services/export.py)
```python
import csv
import json
from typing import List
from pathlib import Path
from ..models.task import Task

class ExportService:
    """Handle exporting tasks to different formats"""
    
    def export_to_json(self, tasks: List[Task], filename: str) -> str:
        """Export tasks to JSON file"""
        Path(filename).parent.mkdir(parents=True, exist_ok=True)
        
        data = []
        for task in tasks:
            task_dict = task.model_dump()
            # Convert dates to strings for JSON
            if task_dict['due_date']:
                task_dict['due_date'] = task_dict['due_date'].isoformat()
            task_dict['created_at'] = task_dict['created_at'].isoformat()
            task_dict['updated_at'] = task_dict['updated_at'].isoformat()
            if task_dict['completed_at']:
                task_dict['completed_at'] = task_dict['completed_at'].isoformat()
            task_dict['tags'] = list(task_dict['tags'])
            data.append(task_dict)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return filename
    
    def export_to_csv(self, tasks: List[Task], filename: str) -> str:
        """Export tasks to CSV file"""
        Path(filename).parent.mkdir(parents=True, exist_ok=True)
        
        fieldnames = [
            'id', 'title', 'description', 'priority', 'status',
            'category', 'tags', 'due_date', 'created_at', 
            'updated_at', 'completed_at'
        ]
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for task in tasks:
                row = task.model_dump()
                # Convert dates to strings
                if row['due_date']:
                    row['due_date'] = row['due_date'].isoformat()
                row['created_at'] = row['created_at'].isoformat()
                row['updated_at'] = row['updated_at'].isoformat()
                if row['completed_at']:
                    row['completed_at'] = row['completed_at'].isoformat()
                row['tags'] = ', '.join(row['tags'])
                writer.writerow(row)
        
        return filename
```

### Analytics Service (src/services/analytics.py)
```python
from typing import Dict, Any, List
from datetime import date, timedelta
from collections import Counter
from ..models.task import Task, Status, Priority

class AnalyticsService:
    """Provide task analytics and insights"""
    
    def get_task_statistics(self, task_manager) -> Dict[str, Any]:
        """Get comprehensive task statistics"""
        tasks = task_manager.get_all_tasks()
        
        if not tasks:
            return {"message": "No tasks found"}
        
        stats = {}
        
        # Basic counts
        stats['total_tasks'] = len(tasks)
        status_counts = task_manager.get_task_count_by_status()
        stats.update({f'{status.value}_tasks': count 
                     for status, count in status_counts.items()})
        
        # Priority distribution
        priority_counts = Counter(task.priority for task in tasks)
        stats['high_priority_tasks'] = priority_counts[Priority.HIGH]
        stats['urgent_tasks'] = priority_counts[Priority.URGENT]
        
        # Due date insights
        overdue_tasks = task_manager.get_overdue_tasks()
        stats['overdue_tasks'] = len(overdue_tasks)
        
        due_soon = [task for task in tasks 
                   if task.due_date and 
                   0 <= (task.due_date - date.today()).days <= 7]
        stats['due_this_week'] = len(due_soon)
        
        # Categories
        categories = task_manager.get_all_categories()
        stats['total_categories'] = len(categories)
        
        # Productivity insights
        completed_tasks = task_manager.get_tasks_by_status(Status.DONE)
        if completed_tasks:
            avg_completion_time = self._calculate_avg_completion_time(completed_tasks)
            stats['avg_completion_days'] = round(avg_completion_time, 1)
        
        return stats
    
    def _calculate_avg_completion_time(self, completed_tasks: List[Task]) -> float:
        """Calculate average time to complete tasks"""
        total_days = 0
        count = 0
        
        for task in completed_tasks:
            if task.completed_at:
                days = (task.completed_at.date() - task.created_at.date()).days
                total_days += days
                count += 1
        
        return total_days / count if count > 0 else 0
    
    def get_productivity_report(self, task_manager, days: int = 30) -> Dict[str, Any]:
        """Generate productivity report for last N days"""
        cutoff_date = date.today() - timedelta(days=days)
        tasks = [task for task in task_manager.get_all_tasks()
                if task.created_at.date() >= cutoff_date]
        
        completed = [task for task in tasks if task.status == Status.DONE]
        
        return {
            'period_days': days,
            'tasks_created': len(tasks),
            'tasks_completed': len(completed),
            'completion_rate': len(completed) / len(tasks) * 100 if tasks else 0,
            'average_daily_creation': len(tasks) / days,
            'average_daily_completion': len(completed) / days
        }
```

---

## 🐳 Docker Configuration

### Dockerfile
```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy project files
COPY pyproject.toml .
COPY src/ src/
COPY tests/ tests/

# Install dependencies
RUN uv sync

# Create data directory
RUN mkdir -p data

# Set up entrypoint
ENTRYPOINT ["uv", "run", "task"]
```

### docker-compose.yml
```yaml
version: '3.8'

services:
  task-manager:
    build: .
    volumes:
      - ./data:/app/data
      - ./src:/app/src
    stdin_open: true
    tty: true
    environment:
      - PYTHONPATH=/app
    command: bash
    
  # For development with hot reload
  dev:
    build: .
    volumes:
      - .:/app
    working_dir: /app
    stdin_open: true
    tty: true
    command: bash
```

---

## 🚀 GitHub Actions CI

### .github/workflows/ci.yml
```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.11', '3.12']
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
    
    - name: Install uv
      uses: astral-sh/setup-uv@v3
      
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v5
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: uv sync --all-extras
    
    - name: Run tests with coverage
      run: uv run pytest tests/ -v --cov=src --cov-report=xml
    
    - name: Run linting
      run: |
        uv run ruff check src/
        uv run black --check src/
        uv run mypy src/
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        
  docker:
    runs-on: ubuntu-latest
    needs: test
    if: github.ref == 'refs/heads/main'
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
    
    - name: Build Docker image
      run: docker build -t task-manager-cli .
    
    - name: Test Docker image
      run: |
        docker run --rm task-manager-cli --help
```

---

## 📋 Usage Examples

### Basic Usage
```bash
# Install dependencies
uv sync --all-extras

# Add tasks
uv run task add "Implement user authentication" --priority urgent --category "Backend" --due 2024-02-15 --tag security --tag api

# List tasks
uv run task list
uv run task list --status todo
uv run task list --overdue
uv run task list --priority high

# Search tasks
uv run task search "authentication"

# Complete a task
uv run task complete <task-id>

# Show statistics
uv run task stats

# Export tasks
uv run task export --format csv --output my_tasks
```

### Docker Usage
```bash
# Build and run with Docker
docker-compose up -d dev
docker-compose exec dev bash

# Inside container
task add "Docker task" --priority high
task list
```

---

## ✅ Week 1 Completion Checklist

### Core Features ✅
- [ ] Task creation with validation
- [ ] Task CRUD operations (Create, Read, Update, Delete)
- [ ] Priority and status management
- [ ] Category and tag system
- [ ] Due date handling with overdue detection
- [ ] Search functionality
- [ ] Export to CSV/JSON

### Technical Requirements ✅
- [ ] Clean class-based architecture
- [ ] Pydantic models for validation
- [ ] Proper error handling
- [ ] File I/O with JSON storage
- [ ] Beautiful CLI with Rich/Typer
- [ ] Comprehensive test suite (80%+ coverage)
- [ ] Type hints throughout
- [ ] Docker containerization

### Quality Standards ✅
- [ ] PEP 8 compliant (ruff + black)
- [ ] Comprehensive documentation
- [ ] GitHub Actions CI/CD
- [ ] Professional project structure
- [ ] Git best practices

---

## 🎓 Learning Outcomes

After completing Week 1, you'll have mastered:

### Core Python Concepts
- **Classes & OOP**: Inheritance, composition, encapsulation
- **Data Structures**: Efficient use of lists, sets, dictionaries
- **File I/O**: JSON serialization, file handling patterns
- **Error Handling**: Try/except, custom exceptions
- **Type Hints**: Static typing for better code quality

### Professional Development
- **Testing**: Unit tests, fixtures, coverage
- **CLI Development**: Modern CLI with Typer/Rich
- **Code Quality**: Linting, formatting, static analysis
- **Project Structure**: Professional Python project layout
- **Package Management**: UV for fast dependency management

### DevOps & Tools
- **Docker**: Containerization best practices
- **CI/CD**: GitHub Actions for automated testing
- **Git Workflow**: Feature branches, meaningful commits
- **Documentation**: README, docstrings, code comments

---

## 🚀 Next Steps

Ready for Week 3? You'll build a **File Processing API** with:
- FastAPI web framework
- Async programming
- File upload/conversion
- Docker Compose with multiple services
- Database integration

This foundation prepares you perfectly for the advanced concepts coming up!