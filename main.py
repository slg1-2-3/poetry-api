from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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