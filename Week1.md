# Week 1: Python Fundamentals & Password Manager Project

## Days 1-3: Core Python Refresher

### Day 1: Variables and Data Types
```python
# Basic data types
name = "Alice"                  # string
age = 25                        # integer
height = 5.6                    # float
is_student = True               # boolean

# Collections
fruits = ["apple", "banana"]    # list (mutable)
coordinates = (10, 20)          # tuple (immutable)
unique_numbers = {1, 2, 3}      # set (unique items)
person = {"name": "Alice", "age": 25}  # dictionary

# Type conversion
str_num = "42"
int_num = int(str_num)          # Convert string to int
float_num = float(str_num)      # Convert string to float
```

### Day 2: Control Flow and Loops
```python
# If statements
score = 85
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
else:
    grade = "C"

# For loops
for fruit in ["apple", "banana", "orange"]:
    print(f"I like {fruit}")

# While loops
count = 0
while count < 5:
    print(count)
    count += 1

# List comprehensions (Pythonic way!)
squares = [x**2 for x in range(10)]
even_squares = [x**2 for x in range(10) if x % 2 == 0]
```

### Day 3: Functions and File I/O
```python
# Functions
def greet(name, greeting="Hello"):
    """Function with default parameter"""
    return f"{greeting}, {name}!"

# Multiple return values
def get_min_max(numbers):
    return min(numbers), max(numbers)

minimum, maximum = get_min_max([1, 5, 3, 9, 2])

# File operations
# Writing to file
with open("data.txt", "w") as f:
    f.write("Hello, World!")

# Reading from file
with open("data.txt", "r") as f:
    content = f.read()

# Working with JSON
import json

data = {"name": "Alice", "age": 25}
# Save to JSON
with open("data.json", "w") as f:
    json.dump(data, f)

# Load from JSON
with open("data.json", "r") as f:
    loaded_data = json.load(f)
```

---

## Days 4-7: Project - Password Manager CLI

### Project Structure
```
password-manager/
├── src/
│   ├── __init__.py
│   ├── password_manager.py
│   ├── encryption.py
│   └── main.py
├── tests/
│   └── test_manager.py
├── data/
│   └── .gitkeep
├── pyproject.toml
├── Dockerfile
├── docker-compose.yml
├── README.md
└── .gitignore
```

### Step 1: Initialize Project with UV

```bash
# Create project directory
mkdir password-manager
cd password-manager

# Initialize with uv
uv init

# Create source directory
mkdir -p src tests data
touch src/__init__.py
```

### Step 2: Configure pyproject.toml

```toml
[project]
name = "password-manager"
version = "0.1.0"
description = "A simple CLI password manager"
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    "click>=8.1.7",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "black>=23.0.0",
    "ruff>=0.1.0",
]

[project.scripts]
pwdmgr = "src.main:cli"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.ruff]
line-length = 88
target-version = "py311"

[tool.black]
line-length = 88
target-version = ["py311"]
```

### Step 3: Install Dependencies

```bash
# Install dependencies using uv
uv sync

# Install with dev dependencies
uv sync --all-extras

# To run commands with uv
uv run python -m src.main
```

### Step 4: Implement Core Classes

```python
# src/password_manager.py
import json
import os
from datetime import datetime
from typing import Dict, List, Optional

class Password:
    """Class to represent a password entry"""
    
    def __init__(self, service: str, username: str, password: str):
        self.service = service
        self.username = username
        self.password = password
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict:
        """Convert password to dictionary"""
        return {
            'service': self.service,
            'username': self.username,
            'password': self.password,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict):
        """TODO: Create Password from dictionary
        
        Hint: Create a new Password instance using data['service'], 
        data['username'], and data['password'].
        Don't forget to set created_at and updated_at from the data!
        """
        pass  # Remove this and implement

class PasswordManager:
    """Main password manager class"""
    
    def __init__(self, storage_file: str = "data/passwords.json"):
        self.storage_file = storage_file
        self.passwords: List[Password] = []
        self.load_passwords()
    
    def load_passwords(self):
        """Load passwords from file"""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r') as f:
                    data = json.load(f)
                    self.passwords = [Password.from_dict(p) for p in data]
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Warning: Could not load passwords file: {e}")
                self.passwords = []
        else:
            self.passwords = []
    
    def save_passwords(self):
        """TODO: Save passwords to file
        
        Steps:
        1. Create directory if it doesn't exist (os.makedirs)
        2. Convert self.passwords to list of dictionaries
        3. Save as JSON with nice formatting (indent=2)
        """
        pass  # Remove this and implement
    
    def add_password(self, service: str, username: str, password: str) -> Password:
        """Add a new password"""
        # Check if already exists
        for pwd in self.passwords:
            if pwd.service.lower() == service.lower() and pwd.username == username:
                raise ValueError(f"Password for {service}/{username} already exists")
        
        new_password = Password(service, username, password)
        self.passwords.append(new_password)
        self.save_passwords()
        return new_password
    
    def get_password(self, service: str, username: Optional[str] = None) -> List[Password]:
        """TODO: Get password(s) for a service
        
        Args:
            service: Name of the service to search for
            username: Optional username to filter by
            
        Returns:
            List of matching Password objects
            
        Hint: Make the service search case-insensitive!
        """
        results = []
        # TODO: Loop through self.passwords
        # TODO: Check if service matches (case-insensitive)
        # TODO: If username provided, also check username
        # TODO: Add matching passwords to results
        return results
    
    def update_password(self, service: str, username: str, new_password: str) -> Password:
        """TODO: Update an existing password
        
        Find the password matching service and username,
        update its password and updated_at timestamp,
        save to file, and return the updated Password.
        
        Raise ValueError if not found.
        """
        pass  # Remove this and implement
    
    def delete_password(self, service: str, username: str) -> bool:
        """Delete a password"""
        for i, pwd in enumerate(self.passwords):
            if pwd.service.lower() == service.lower() and pwd.username == username:
                del self.passwords[i]
                self.save_passwords()
                return True
        return False
    
    def list_all_services(self) -> List[str]:
        """TODO: List all unique services
        
        Return a sorted list of all unique service names.
        Hint: Use a set to get unique values, then sort!
        """
        pass  # Remove this and implement
```

### Step 5: Simple Encryption (Educational Only!)

```python
# src/encryption.py
import base64

class SimpleEncryption:
    """
    Simple XOR encryption for learning purposes.
    ⚠️ NOT SECURE - Don't use for real passwords!
    """
    
    def __init__(self, key: str = "mysecretkey"):
        self.key = key
    
    def encrypt(self, text: str) -> str:
        """TODO: Encrypt text using XOR
        
        Steps:
        1. Create empty list for encrypted bytes
        2. For each character in text:
           - Get its ASCII value (ord)
           - XOR with corresponding key character
           - Use modulo to cycle through key
        3. Convert to bytes and encode as base64
        
        Example:
        text[i] XOR key[i % len(key)]
        """
        encrypted = []
        for i, char in enumerate(text):
            # TODO: XOR character with key character
            # key_char = self.key[i % len(self.key)]
            # encrypted_char = ord(char) ^ ord(key_char)
            # encrypted.append(encrypted_char)
            pass
        
        # TODO: Convert to base64
        # return base64.b64encode(bytes(encrypted)).decode('utf-8')
        return text  # Remove this line
    
    def decrypt(self, encrypted: str) -> str:
        """TODO: Decrypt text
        
        XOR encryption is symmetric, so decryption is the same process!
        1. Decode from base64
        2. XOR each byte with key
        3. Convert back to string
        """
        pass  # Remove this and implement
```

### Step 6: CLI Interface

```python
# src/main.py
import click
import getpass
from password_manager import PasswordManager

@click.group()
def cli():
    """Simple Password Manager CLI"""
    pass

@cli.command()
@click.option('--service', prompt=True, help='Service name (e.g., Gmail)')
@click.option('--username', prompt=True, help='Username or email')
@click.option('--password', prompt=True, hide_input=True, help='Password')
def add(service, username, password):
    """Add a new password"""
    manager = PasswordManager()
    try:
        pwd = manager.add_password(service, username, password)
        click.echo(f"✅ Password added for {service}")
    except ValueError as e:
        click.echo(f"❌ Error: {e}", err=True)

@cli.command()
@click.option('--service', prompt=True, help='Service name')
@click.option('--username', default=None, help='Username (optional)')
def get(service, username):
    """Get password for a service"""
    manager = PasswordManager()
    passwords = manager.get_password(service, username)
    
    if not passwords:
        click.echo(f"No passwords found for {service}")
        return
    
    click.echo(f"\n📔 Passwords for {service}:")
    for pwd in passwords:
        click.echo(f"  Username: {pwd.username}")
        click.echo(f"  Password: {pwd.password}")
        click.echo(f"  Updated: {pwd.updated_at}\n")

@cli.command()
def list():
    """List all services"""
    manager = PasswordManager()
    services = manager.list_all_services()
    
    if services:
        click.echo("\n📋 Stored services:")
        for service in services:
            passwords = manager.get_password(service)
            click.echo(f"  • {service} ({len(passwords)} account(s))")
    else:
        click.echo("No passwords stored yet")

@cli.command()
@click.option('--service', prompt=True, help='Service name')
@click.option('--username', prompt=True, help='Username')
def delete(service, username):
    """Delete a password"""
    manager = PasswordManager()
    if click.confirm(f"Delete password for {service}/{username}?"):
        if manager.delete_password(service, username):
            click.echo(f"✅ Password deleted")
        else:
            click.echo(f"❌ Password not found")

if __name__ == '__main__':
    cli()
```

### Step 7: Write Tests

```python
# tests/test_manager.py
import pytest
import os
import tempfile
import json
from src.password_manager import PasswordManager, Password

def test_password_to_dict():
    """Test Password.to_dict method"""
    pwd = Password("gmail", "user@test.com", "secret123")
    data = pwd.to_dict()
    
    assert data['service'] == 'gmail'
    assert data['username'] == 'user@test.com'
    assert data['password'] == 'secret123'
    assert 'created_at' in data
    assert 'updated_at' in data

def test_password_from_dict():
    """TODO: Test Password.from_dict method
    
    Create a dictionary with password data,
    use from_dict to create a Password object,
    assert all fields are correct.
    """
    data = {
        'service': 'github',
        'username': 'dev@test.com',
        'password': 'ghp_token123',
        'created_at': '2024-01-01T10:00:00',
        'updated_at': '2024-01-01T10:00:00'
    }
    # TODO: Create Password using from_dict
    # TODO: Assert all fields match
    pass

def test_add_password():
    """Test adding a password"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_file = f.name
    
    try:
        manager = PasswordManager(temp_file)
        pwd = manager.add_password("github", "developer", "pass123")
        
        assert pwd.service == "github"
        assert pwd.username == "developer"
        assert len(manager.passwords) == 1
        
        # Check file was created
        assert os.path.exists(temp_file)
        
        # Check duplicate prevention
        with pytest.raises(ValueError):
            manager.add_password("github", "developer", "newpass")
    finally:
        os.unlink(temp_file)

def test_get_password():
    """TODO: Test getting passwords
    
    1. Create manager with temp file
    2. Add 2-3 passwords
    3. Test getting by service
    4. Test getting by service + username
    5. Test case-insensitive search
    """
    pass

def test_list_all_services():
    """TODO: Test listing services
    
    1. Add passwords for different services
    2. Add multiple passwords for same service
    3. Check list returns unique, sorted services
    """
    pass

# Run tests with: uv run pytest tests/
```

### Step 8: Docker Setup

```dockerfile
# Dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy project files
COPY pyproject.toml .
COPY src/ src/

# Install dependencies
RUN uv sync

# Run the CLI
CMD ["uv", "run", "python", "-m", "src.main"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    build: .
    volumes:
      - ./src:/app/src
      - ./data:/app/data
      - ./tests:/app/tests
    stdin_open: true
    tty: true
    command: /bin/bash
```

### Step 9: GitHub Actions CI

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Install uv
      uses: astral-sh/setup-uv@v3
      
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.12'
    
    - name: Install dependencies
      run: uv sync --all-extras
    
    - name: Run tests
      run: uv run pytest tests/ -v
    
    - name: Run linting
      run: |
        uv run ruff check src/
        uv run black --check src/
```

### Usage Examples

```bash
# Install dependencies
uv sync

# Add a password
uv run python -m src.main add

# List all services
uv run python -m src.main list

# Get a specific password
uv run python -m src.main get --service github

# Delete a password
uv run python -m src.main delete --service github --username myuser

# Run tests
uv run pytest tests/ -v

# Format code
uv run black src/
uv run ruff check src/ --fix

# Using Docker
docker-compose up -d
docker-compose exec app bash
# Inside container:
uv run python -m src.main add
```

## Tasks to Complete ✅

### Required (Must Do)
1. [ ] Implement `Password.from_dict()` method
2. [ ] Implement `save_passwords()` method  
3. [ ] Implement `get_password()` method
4. [ ] Implement `update_password()` method
5. [ ] Implement `list_all_services()` method
6. [ ] Write test for `test_password_from_dict()`
7. [ ] Write test for `test_get_password()`
8. [ ] Write test for `test_list_all_services()`

### Optional (Bonus Challenges)
9. [ ] Implement encryption methods in `SimpleEncryption`
10. [ ] Add password strength checker
11. [ ] Add random password generator
12. [ ] Add export to CSV functionality
13. [ ] Add import from CSV functionality
14. [ ] Add search functionality (search in all fields)
15. [ ] Add update command to CLI

## Learning Goals for Week 1

By the end of this week, you should understand:
- ✅ Python data types and when to use each
- ✅ How to work with files and JSON
- ✅ Writing and using classes
- ✅ List comprehensions
- ✅ Exception handling with try/except
- ✅ Using UV package manager
- ✅ Writing basic tests with pytest
- ✅ Creating CLI applications with Click
- ✅ Docker basics for Python projects

## Tips for Success

1. **Start Simple**: Get the basic functionality working before adding features
2. **Test Often**: Run your code frequently to catch errors early
3. **Use Type Hints**: They help catch bugs and make code clearer
4. **Read Error Messages**: Python errors are usually very helpful
5. **Commit Often**: Use git to save your progress frequently

## Common Issues & Solutions

**Issue**: `ModuleNotFoundError: No module named 'src'`
**Solution**: Make sure you have `__init__.py` in src folder and run with `uv run python -m src.main`

**Issue**: JSON decode error when loading passwords
**Solution**: Check if the JSON file is valid, or delete it and start fresh

**Issue**: Tests not finding the module
**Solution**: Run tests with `uv run pytest` from project root

## Next Week Preview

Week 2 will cover:
- Important CS concepts (Big O notation, data structures)
- Working with APIs using Flask
- Understanding time complexity
- Basic algorithms (searching and sorting)
- Building a Todo List API with proper REST endpoints