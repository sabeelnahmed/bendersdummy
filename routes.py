from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Initialize router
router = APIRouter()

# Data models
class Item(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    price: float
    created_at: Optional[str] = None

class User(BaseModel):
    id: Optional[int] = None
    username: str
    email: str
    full_name: Optional[str] = None

# In-memory databases
items_db: List[Item] = []
users_db: List[User] = []
item_counter = 1
user_counter = 1

# Root endpoint
@router.get("/")
async def root():
    return {
        "message": "Welcome to the Dummy Backend API",
        "endpoints": {
            "docs": "/docs",
            "items": "/items",
            "users": "/users"
        }
    }

# Health check
@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

# Items endpoints
@router.get("/items", response_model=List[Item])
async def get_items():
    """Get all items"""
    return items_db

@router.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int):
    """Get a specific item by ID"""
    for item in items_db:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@router.post("/items", response_model=Item, status_code=201)
async def create_item(item: Item):
    """Create a new item"""
    global item_counter
    item.id = item_counter
    item.created_at = datetime.now().isoformat()
    items_db.append(item)
    item_counter += 1
    return item

@router.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, updated_item: Item):
    """Update an existing item"""
    for idx, item in enumerate(items_db):
        if item.id == item_id:
            updated_item.id = item_id
            updated_item.created_at = item.created_at
            items_db[idx] = updated_item
            return updated_item
    raise HTTPException(status_code=404, detail="Item not found")

@router.delete("/items/{item_id}")
async def delete_item(item_id: int):
    """Delete an item"""
    for idx, item in enumerate(items_db):
        if item.id == item_id:
            items_db.pop(idx)
            return {"message": f"Item {item_id} deleted successfully"}
    raise HTTPException(status_code=404, detail="Item not found")

# Users endpoints
@router.get("/users", response_model=List[User])
async def get_users():
    """Get all users"""
    return users_db

@router.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    """Get a specific user by ID"""
    for user in users_db:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

@router.post("/users", response_model=User, status_code=201)
async def create_user(user: User):
    """Create a new user"""
    global user_counter
    user.id = user_counter
    users_db.append(user)
    user_counter += 1
    return user

@router.delete("/users/{user_id}")
async def delete_user(user_id: int):
    """Delete a user"""
    for idx, user in enumerate(users_db):
        if user.id == user_id:
            users_db.pop(idx)
            return {"message": f"User {user_id} deleted successfully"}
    raise HTTPException(status_code=404, detail="User not found")

