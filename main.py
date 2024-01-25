import os
from dotenv import load_dotenv

from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import crud, models, schemas, security
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

load_dotenv('security_secrets.env')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# user functions

@app.get("/users/me")
def read_current_user(username: Annotated[str, Depends(security.get_current_user)]):
    return {"username": username}
        
@app.post("/users/", response_model=schemas.UserInfo)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)) -> schemas.Token:
    form_data.password = security.hash_password(form_data.password)
    db_user = crud.get_user(db=db,user=form_data)
    if not db_user:
        raise HTTPException(status_code=400, detail="Incorrect Username or Password")
    import pdb; pdb.set_trace()
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": db_user.username}, expires_delta=access_token_expires
        )
    return schemas.Token(access_token=access_token, token_type="bearer")


# author functions

@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db=db, author=author)


@app.patch("/authors/{author_id}", response_model=schemas.Author)
def update_author(author_id: str, author_patch: schemas.AuthorUpdate, db: Session = Depends(get_db)):
    return crud.update_author(db=db, id=author_id, author_patch=author_patch)

@app.get("/authors/", response_model=list[schemas.Author])
def get_authors(db: Session = Depends(get_db)):
    authors = crud.get_authors(db)
    return authors

@app.get("/authors/{author_id}", response_model=schemas.Author)
def get_author_by_id(author_id: str, db: Session = Depends(get_db)):
    author = crud.get_author_by_id(db=db, id=author_id)
    return author

@app.delete("/authors/{author_id}")
def delete_author_by_id(author_id: str, db: Session = Depends(get_db)):
    author = crud.delete_author_by_id(db=db, author_id=author_id)
    return HTTPException(status_code=204, detail="Deleted successfully, no data returned")

# poem functions

@app.get("/poems/", response_model=list[schemas.PoemBase], response_model_exclude_none=False)
def get_poems(db: Session = Depends(get_db)):
    poems = crud.get_poems(db)
    return poems

@app.get("/poems/{poem_id}", response_model=schemas.Poem)
def get_poem_by_id(poem_id: str, db: Session = Depends(get_db)):
    poem = crud.get_poem_by_id(db=db, id=poem_id)
    return poem

@app.post("/poems/", response_model=schemas.Poem, response_model_exclude_none=True)
def create_poem(author_id: str, poem: schemas.PoemCreate, db: Session = Depends(get_db)):
    poem = crud.create_poem(db=db, poem=poem, author_id=author_id)
    return poem

@app.patch("/poems/{poem_id}", response_model=schemas.PoemUpdate)
def update_poem(poem_id: str, poem: schemas.PoemUpdate, db: Session = Depends(get_db)):
    poem = crud.update_poem(db=db, poem_update=poem, poem_id=poem_id )
    return poem

@app.delete("/poems/{poem_id}")
def delete_poem_by_id(poem_id: str, db: Session =Depends(get_db)):
    poem = crud.delete_poem_by_id(db=db, poem_id=poem_id)
    return HTTPException(status_code=204, detail="Deleted successfully, no data returned")