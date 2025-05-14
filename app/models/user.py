<<<<<<< HEAD
from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    fullName: Optional[str] = None
    email: str
    role: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class UserInDB(UserBase):
    id: int
    password: str

class User(UserBase):
    id: int

    class Config:
        from_attributes = True 
=======
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    fullName = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(50), default="user")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    courses = relationship("Course", back_populates="user", cascade="all, delete-orphan")
    quizzes = relationship("Quiz", back_populates="user", cascade="all, delete-orphan") 
>>>>>>> ebc48618dcd9e3a24147d544fd18df0fae58d4fd
