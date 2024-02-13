from datetime import datetime, timedelta, timezone

from typing import Annotated
import hashlib
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import (OAuth2PasswordBearer,
                              OAuth2PasswordRequestForm,
                              SecurityScopes)
from sqlalchemy.orm import Session

import os
from dotenv import load_dotenv
import schemas, crud
from database import SessionLocal



# separating the user security stuff here for now

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={"me": "Read information about the current user"}
    )

load_dotenv('security_secrets.env')
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()
    
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(
        security_scopes: SecurityScopes, token: Annotated[str, Depends(oauth2_scheme)]
):
    if security_scopes.scopes: 
        authenticate_value = f'Bearer scope"{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    credentials_exeption = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value}
    )
    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exeption
        token_scopes = payload.get("scopes", [])
        token_data = schemas.TokenData(scopes=token_scopes, username=username)
    except (JWTError, schemas.ValidationError):
        raise credentials_exeption
    user = crud.check_username(db=SessionLocal(), username=token_data.username)
    if user is None:
        raise credentials_exeption
    for scope in security_scopes.scopes:                      
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": authenticate_value}
            )
        return user

async def get_current_active_user(
        
)