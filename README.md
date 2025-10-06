# Dummy Backend Server

A simple dummy backend server built with FastAPI for testing and development purposes.

## Features

- ✅ RESTful API with CRUD operations
- ✅ Items management (Create, Read, Update, Delete)
- ✅ Users management (Create, Read, Delete)
- ✅ In-memory database (data resets on server restart)
- ✅ Interactive API documentation (Swagger UI)
- ✅ Health check endpoint

## Setup

### 1. Activate Virtual Environment

```bash
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

## Running the Server

### Option 1: Using Python directly

```bash
python main.py
```

### Option 2: Using Uvicorn

```bash
uvicorn main:app --reload
```

The server will start at `http://localhost:8000`

## API Endpoints

### Root
- `GET /` - Welcome message and available endpoints

### Health Check
- `GET /health` - Server health status

### Items
- `GET /items` - Get all items
- `GET /items/{item_id}` - Get a specific item
- `POST /items` - Create a new item
- `PUT /items/{item_id}` - Update an existing item
- `DELETE /items/{item_id}` - Delete an item

### Users
- `GET /users` - Get all users
- `GET /users/{user_id}` - Get a specific user
- `POST /users` - Create a new user
- `DELETE /users/{user_id}` - Delete a user

## Interactive Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Example Requests

### Create an Item

```bash
curl -X POST "http://localhost:8000/items" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Laptop",
    "description": "Gaming laptop",
    "price": 1299.99
  }'
```

### Get All Items

```bash
curl http://localhost:8000/items
```

### Create a User

```bash
curl -X POST "http://localhost:8000/users" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "full_name": "John Doe"
  }'
```

### Get All Users

```bash
curl http://localhost:8000/users
```

## Data Models

### Item
```python
{
  "id": int,           # Auto-generated
  "name": str,         # Required
  "description": str,  # Optional
  "price": float,      # Required
  "created_at": str    # Auto-generated
}
```

### User
```python
{
  "id": int,           # Auto-generated
  "username": str,     # Required
  "email": str,        # Required
  "full_name": str     # Optional
}
```

## Development

To stop the server, press `Ctrl+C` in the terminal.

To deactivate the virtual environment:
```bash
deactivate
```

## Tech Stack

- **FastAPI** - Modern, fast web framework for building APIs
- **Uvicorn** - ASGI server for running the application
- **Pydantic** - Data validation using Python type annotations

