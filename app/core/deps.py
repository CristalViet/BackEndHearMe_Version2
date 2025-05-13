from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import SessionLocal
from app.services.auth import SECRET_KEY, ALGORITHM
from app.schemas.user import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/token")

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    
    result = db.execute(
        text("SELECT id, email, fullName, role FROM users WHERE email = :email"),
        {"email": token_data.email}
    )
    user = result.fetchone()
    
    if user is None:
        raise credentials_exception

    # Convert SQLAlchemy Row to dictionary
    user_dict = {
        "id": user.id,
        "email": user.email,
        "fullName": user.fullName,
        "role": user.role
    }
    
    return user_dict

def get_current_active_user(
    current_user = Depends(get_current_user),
):
    return current_user 