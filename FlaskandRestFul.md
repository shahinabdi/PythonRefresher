# Flask RESTful API Learning Project

A comprehensive project to learn Flask, RESTful APIs, PostgreSQL, Docker, and Design Patterns.

## 📋 Prerequisites

- Docker and Docker Compose installed
- Python 3.11+
- UV package manager (`curl -LsSf https://astral.sh/uv/install.sh | sh`)

## 🚀 Project Structure

```
flask-rest-project/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── users.py
│   │   └── products.py
│   └── utils/
│       ├── __init__.py
│       └── database_singleton.py
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
├── .env.example
└── README.md
```

## 🛠️ Initial Setup

### 1. Initialize the Project

```bash
# Create project directory
mkdir flask-rest-project
cd flask-rest-project

# Initialize UV project
uv init

# Add dependencies
uv add flask flask-sqlalchemy psycopg2-binary python-dotenv
```

### 2. Environment Configuration

Create a `.env` file:

```env
POSTGRES_USER=student
POSTGRES_PASSWORD=student123
POSTGRES_DB=flask_learning
DATABASE_URL=postgresql://student:student123@db:5432/flask_learning
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
```

### 3. Docker Configuration

**Dockerfile**:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install UV
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy project files
COPY pyproject.toml .
COPY uv.lock* .

# Install dependencies
RUN uv sync --frozen

# Copy application code
COPY . .

EXPOSE 5000

CMD ["uv", "run", "python", "-m", "flask", "run", "--host=0.0.0.0"]
```

**docker-compose.yml**:
```yaml
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U student"]
      interval: 5s
      timeout: 5s
      retries: 5

  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      DATABASE_URL: ${DATABASE_URL}
      FLASK_ENV: ${FLASK_ENV}
      SECRET_KEY: ${SECRET_KEY}
    depends_on:
      db:
        condition: service_healthy
    volumes:
      - .:/app
    command: uv run python -m flask run --host=0.0.0.0

volumes:
  postgres_data:
```

## 📚 Code Implementation

### 1. Database Singleton Pattern (Example)

**app/utils/database_singleton.py**:
```python
"""
Singleton Pattern Example: Database Connection Manager
Ensures only one database connection instance exists throughout the application.
"""

class DatabaseSingleton:
    _instance = None
    _connection = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseSingleton, cls).__new__(cls)
        return cls._instance
    
    def get_connection(self):
        """Returns the database connection"""
        return self._connection
    
    def set_connection(self, connection):
        """Sets the database connection"""
        self._connection = connection
```

### 2. Configuration (Example)

**app/config.py**:
```python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

### 3. Database Setup (Example)

**app/database.py**:
```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    """Initialize the database"""
    db.init_app(app)
    with app.app_context():
        db.create_all()
```

### 4. User Model (Example)

**app/models/user.py**:
```python
from app.database import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }
```

### 5. Flask App Initialization (Example)

**app/__init__.py**:
```python
from flask import Flask
from app.config import Config
from app.database import db, init_db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize database
    init_db(app)
    
    # Register blueprints
    from app.routes.users import users_bp
    from app.routes.products import products_bp
    
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(products_bp, url_prefix='/api/products')
    
    return app
```

## 🎯 RESTful Routes Examples and Exercises

### GET Routes

#### Example 1: Get All Users
**app/routes/users.py**:
```python
from flask import Blueprint, jsonify
from app.models.user import User

users_bp = Blueprint('users', __name__)

@users_bp.route('/', methods=['GET'])
def get_users():
    """GET Example: Retrieve all users"""
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200
```

#### Exercise 1: Get User by ID
```python
@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """
    TODO: Implement GET route to retrieve a single user by ID
    
    Hints:
    - Use User.query.get(user_id) or User.query.filter_by(id=user_id).first()
    - Return 404 if user not found
    - Return user data with 200 status code if found
    """
    pass  # Complete this function
```

#### Exercise 2: Search Users by Username
```python
@users_bp.route('/search', methods=['GET'])
def search_users():
    """
    TODO: Implement search functionality using query parameters
    
    Hints:
    - Get 'username' from request.args
    - Use User.query.filter(User.username.contains(search_term)).all()
    - Return list of matching users
    - Example: GET /api/users/search?username=john
    """
    pass  # Complete this function
```

---

### POST Routes

#### Example 1: Create User
```python
from flask import request

@users_bp.route('/', methods=['POST'])
def create_user():
    """POST Example: Create a new user"""
    data = request.get_json()
    
    # Validation
    if not data or 'username' not in data or 'email' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Create user
    user = User(username=data['username'], email=data['email'])
    db.session.add(user)
    db.session.commit()
    
    return jsonify(user.to_dict()), 201
```

#### Exercise 1: Create Product
**app/routes/products.py**:
```python
from flask import Blueprint, request, jsonify

products_bp = Blueprint('products', __name__)

@products_bp.route('/', methods=['POST'])
def create_product():
    """
    TODO: Implement POST route to create a new product
    
    Hints:
    - Get JSON data from request.get_json()
    - Validate required fields: name, price, description
    - Create Product model instance (you need to create this model first)
    - Add to db.session and commit
    - Return created product with 201 status
    
    Expected JSON body:
    {
        "name": "Product Name",
        "price": 29.99,
        "description": "Product description"
    }
    """
    pass  # Complete this function
```

#### Exercise 2: Bulk Create Users
```python
@users_bp.route('/bulk', methods=['POST'])
def bulk_create_users():
    """
    TODO: Create multiple users at once
    
    Hints:
    - Expect a list of user objects in request body
    - Validate each user has required fields
    - Use db.session.add_all() for efficiency
    - Return list of created users with 201 status
    
    Expected JSON body:
    {
        "users": [
            {"username": "user1", "email": "user1@example.com"},
            {"username": "user2", "email": "user2@example.com"}
        ]
    }
    """
    pass  # Complete this function
```

---

### PUT Routes

#### Example 1: Update User
```python
@users_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """PUT Example: Update an existing user (full update)"""
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    
    # Update fields
    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    
    db.session.commit()
    
    return jsonify(user.to_dict()), 200
```

#### Exercise 1: Update Product
```python
@products_bp.route('/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """
    TODO: Implement PUT route to update a product
    
    Hints:
    - Find product by ID
    - Return 404 if not found
    - Update all fields from request data
    - Commit changes to database
    - Return updated product with 200 status
    """
    pass  # Complete this function
```

#### Exercise 2: Update User Email Only
```python
@users_bp.route('/<int:user_id>/email', methods=['PUT'])
def update_user_email(user_id):
    """
    TODO: Update only the email field of a user
    
    Hints:
    - Find user by ID
    - Validate new email is provided
    - Check if email is already in use (unique constraint)
    - Update only email field
    - Return updated user
    """
    pass  # Complete this function
```

---

### PATCH Routes

#### Example 1: Partial Update User
```python
@users_bp.route('/<int:user_id>', methods=['PATCH'])
def patch_user(user_id):
    """PATCH Example: Partially update a user"""
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    
    # Update only provided fields
    if 'username' in data:
        user.username = data['username']
    if 'email' in data:
        user.email = data['email']
    
    db.session.commit()
    
    return jsonify(user.to_dict()), 200
```

#### Exercise 1: Patch Product Price
```python
@products_bp.route('/<int:product_id>/price', methods=['PATCH'])
def update_product_price(product_id):
    """
    TODO: Update only the price of a product
    
    Hints:
    - Find product by ID
    - Validate price is provided and is a valid number
    - Update only the price field
    - Don't allow negative prices
    - Return updated product
    """
    pass  # Complete this function
```

#### Exercise 2: Toggle User Active Status
```python
@users_bp.route('/<int:user_id>/toggle-active', methods=['PATCH'])
def toggle_user_active(user_id):
    """
    TODO: Toggle user's active status
    
    Hints:
    - Add 'is_active' boolean field to User model first
    - Find user by ID
    - Toggle the is_active field (True -> False or False -> True)
    - Return updated user
    """
    pass  # Complete this function
```

---

### DELETE Routes

#### Example 1: Delete User
```python
@users_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """DELETE Example: Delete a user"""
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({'message': 'User deleted successfully'}), 200
```

#### Exercise 1: Delete Product
```python
@products_bp.route('/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """
    TODO: Implement DELETE route to remove a product
    
    Hints:
    - Find product by ID
    - Return 404 if not found
    - Delete from database using db.session.delete()
    - Commit changes
    - Return success message with 200 status
    """
    pass  # Complete this function
```

#### Exercise 2: Delete All Users (with confirmation)
```python
@users_bp.route('/delete-all', methods=['DELETE'])
def delete_all_users():
    """
    TODO: Delete all users (dangerous operation!)
    
    Hints:
    - Require a confirmation parameter: ?confirm=yes
    - Check request.args.get('confirm')
    - Only proceed if confirmation is 'yes'
    - Use User.query.delete() to delete all
    - Return count of deleted users
    - Return 400 if confirmation not provided
    """
    pass  # Complete this function
```

---

## 🏗️ Additional Exercise: Create Product Model

**app/models/product.py**:
```python
"""
TODO: Create the Product model

Hints:
- Import db from app.database
- Create Product class that inherits from db.Model
- Add fields: id (Integer, primary_key), name (String, not null), 
  price (Float, not null), description (Text), created_at (DateTime)
- Implement to_dict() method like in User model
"""

# Your code here
```

## 🚀 Running the Project

### Start the Application

```bash
# Build and start containers
docker-compose up --build

# In another terminal, create tables
docker-compose exec web uv run python -c "from app import create_app; app = create_app(); app.app_context().push(); from app.database import db; db.create_all()"
```

### Test the API

```bash
# Create a user
curl -X POST http://localhost:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{"username":"john_doe","email":"john@example.com"}'

# Get all users
curl http://localhost:5000/api/users

# Get user by ID
curl http://localhost:5000/api/users/1

# Update user
curl -X PUT http://localhost:5000/api/users/1 \
  -H "Content-Type: application/json" \
  -d '{"username":"jane_doe","email":"jane@example.com"}'

# Delete user
curl -X DELETE http://localhost:5000/api/users/1
```

## 📝 Learning Objectives

By completing this project, students will learn:

1. ✅ **Flask Basics**: Creating routes, handling requests/responses
2. ✅ **RESTful API Design**: HTTP methods (GET, POST, PUT, PATCH, DELETE)
3. ✅ **Database Integration**: SQLAlchemy ORM with PostgreSQL
4. ✅ **Design Patterns**: Singleton pattern for database management
5. ✅ **Containerization**: Docker and Docker Compose
6. ✅ **Modern Python Tooling**: UV package manager
7. ✅ **API Testing**: Using curl or Postman

## 🎓 Exercises Summary

- **GET**: 2 exercises (get by ID, search)
- **POST**: 2 exercises (create product, bulk create)
- **PUT**: 2 exercises (update product, update email)
- **PATCH**: 2 exercises (update price, toggle status)
- **DELETE**: 2 exercises (delete product, delete all)
- **Model Creation**: 1 exercise (Product model)

## 🔍 Tips for Students

1. Start with the examples to understand the pattern
2. Read the hints carefully in each exercise
3. Test your code using curl or Postman
4. Check database changes using a PostgreSQL client
5. Don't forget error handling (404, 400, etc.)
6. Always validate input data before processing

## 📚 Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [RESTful API Best Practices](https://restfulapi.net/)
- [UV Documentation](https://docs.astral.sh/uv/)

---

Happy Learning! 🚀