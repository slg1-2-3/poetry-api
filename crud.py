from sqlalchemy.orm import Session
from sqlalchemy import insert, delete, update
import models, schemas

# author cruds

def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.Author(firstname=author.firstname, lastname=author.lastname)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

def get_authors(db: Session, skip: int=0, limit: int=100): 
    return db.query(models.Author).offset(skip).limit(limit).all()

def get_author_by_id(db: Session, id: int):
    return db.query(models.Author).filter(models.Author.id == id).first()

def update_author(db: Session, id: int, author_patch: schemas.AuthorUpdate):
    author = db.query(models.Author).filter(models.Author.id == id).first()
    if author:
        for field, value in author_patch.model_dump(exclude_unset=True).items():
            setattr(author, field, value)
        db.commit()
        db.refresh(author)
    return author

def delete_author_by_id(db: Session, author_id:int) : 
    author = db.query(models.Author).filter(models.Author.id == author_id).first()
    poems = db.query(models.Poem).filter(models.Poem.author_id == author_id).all()
    if author: 
        if poems:
            for poem in poems:
                db.delete(poem) 
        db.delete(author)
        db.commit()

# poem cruds

def get_poem_by_id(db: Session, id: int):
    return db.query(models.Poem).filter(models.Poem.id == id).first()

def get_poems(db: Session, skip: int=0, limit: int=100):
    return db.query(models.Poem).offset(skip).limit(limit).all()

def create_poem(db: Session, poem: schemas.PoemCreate, author_id: int):
    db_poem = models.Poem(**poem.model_dump(exclude_none=True), author_id=author_id)
    db.add(db_poem)
    db.commit()
    db.refresh(db_poem)
    return db_poem

def update_poem(db: Session, poem_update: schemas.PoemUpdate, poem_id: int):
    poem = db.query(models.Poem).filter(models.Poem.id == poem_id).first()
    if poem:
        for field, value in poem_update.model_dump(exclude_none=True).items():
            setattr(poem, field, value)
        db.commit()
        db.refresh(poem)
    return poem 

def delete_poem_by_id(db: Session, poem_id: int):
    poem = db.query(models.Poem).filter(models.Poem.id == poem_id).first()
    if poem: 
        db.delete(poem)
        db.commit()
