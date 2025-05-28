from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel

router = APIRouter()

# Định nghĩa model cho request/response
class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

# Fake database
fake_users_db = []

# API endpoints
@router.post("/users/", response_model=User)
async def create_user(user: UserCreate):
    """Tạo user mới"""
    # Kiểm tra user đã tồn tại chưa
    if any(u["email"] == user.email for u in fake_users_db):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Tạo user mới
    db_user = {
        "id": len(fake_users_db) + 1,
        "username": user.username,
        "email": user.email,
        "is_active": True
    }
    fake_users_db.append(db_user)
    return db_user

@router.get("/users/", response_model=List[User])
async def read_users(skip: int = 0, limit: int = 10):
    """Lấy danh sách users"""
    return fake_users_db[skip : skip + limit]

@router.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int):
    """Lấy thông tin user theo ID"""
    for user in fake_users_db:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

@router.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, user: UserBase):
    """Cập nhật thông tin user"""
    for index, stored_user in enumerate(fake_users_db):
        if stored_user["id"] == user_id:
            # Cập nhật thông tin
            fake_users_db[index].update({
                "username": user.username,
                "email": user.email
            })
            return fake_users_db[index]
    raise HTTPException(status_code=404, detail="User not found")

@router.delete("/users/{user_id}")
async def delete_user(user_id: int):
    """Xóa user"""
    for index, user in enumerate(fake_users_db):
        if user["id"] == user_id:
            fake_users_db.pop(index)
            return {"message": "User deleted successfully"}
    raise HTTPException(status_code=404, detail="User not found") 