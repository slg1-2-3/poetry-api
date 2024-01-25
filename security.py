from datetime import datetime, timedelta, timezone

from typing import Annotated
import hashlib
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import os
from dotenv import load_dotenv
import models, schemas

# separating the user security stuff here for now

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

load_dotenv('security_secrets.env')
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def get_user(db: Session, username:str):
    user = db.query(models.User).filter(models.User.username == username).first()
    if user:
        return user
    
def fake_decode_token(token, db: Session):
    user = get_user(token, db=db)
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exeption = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exeption
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exeption
    user = get_user(db=Session, username=token_data.username)
    if user is None:
        raise credentials_exeption
    return user

