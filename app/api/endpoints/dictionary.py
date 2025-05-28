from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.dictionary import Words
from typing import List
from pydantic import BaseModel
router = APIRouter()

# Model cho response
class Word(BaseModel):
    id: int
    word: str
    meaning: str
    type: str
    linkVideo:str
    linkThumbnail:str
    class Config:
        from_attributes = True

# API endpoint để lấy danh sách từ
@router.get("/words", response_model=List[Word])
async def get_words(skip: int=0, limit:int=10, db: Session = Depends(get_db)):
    words = db.query(Words).offset(skip).limit(limit).all()
    return words

# API endpoint để tìm kiếm từ
@router.get("/words/search", response_model=List[Word])
async def search_words(query: str, skip: int=0, limit: int=10, db: Session = Depends(get_db)):
    if not query or query.strip() == "":
        raise HTTPException(status_code=400, detail="Query parameter cannot be empty")
    
    if query == "${query}":
        raise HTTPException(status_code=400, detail="Invalid query parameter. Please provide a valid search term")
    
    print(f"Searching for words containing: {query}")
    words = db.query(Words).filter(Words.word.ilike(f"%{query}%")).offset(skip).limit(limit).all()
    print(f"Found {len(words)} results")
    return words
@router.get("/words/{word_id}", response_model=Word)
async def get_word(word: str, ):
    return True
    


