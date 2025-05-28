from sqlalchemy import Column, Integer, String, Text
from app.database.database import Base

class Words(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True, index=True)
    word = Column(String(100), unique=True, index=True)
    linkThumbnail = Column(String(255), nullable=True)
    linkVideo = Column(String(255), nullable=True)
    meaning = Column(Text)
    type = Column(String(50))  # noun, verb, adjective, etc.
