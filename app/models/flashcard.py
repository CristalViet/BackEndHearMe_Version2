from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.base import Base

class Course(Base):
    __tablename__ = "courses"

    course_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    nameschool = Column(String(255))
    namecourse = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    quizzes = relationship("Quiz", back_populates="course", cascade="all, delete-orphan")
    user = relationship("User", back_populates="courses")

class Quiz(Base):
    __tablename__ = "quizzes"

    quizzes_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.course_id", ondelete="CASCADE"), nullable=False)
    definition = Column(Text, nullable=False)
    mota = Column(Text, nullable=False)
    image = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    course = relationship("Course", back_populates="quizzes")
    user = relationship("User", back_populates="quizzes") 