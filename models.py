import uuid
from sqlalchemy import Boolean, Column, ForeignKey, String, Text
from sqlalchemy.orm import relationship

from database import Base

def generate_uuid():
    return str(uuid.uuid4())

class Author(Base):
    __tablename__ = 'authors'

    id = Column(String(100), primary_key=True, default=generate_uuid)
    firstname = Column(String(100))
    lastname = Column(String(100))

    poems = relationship("Poem", back_populates="authors")

class Poem(Base):
    __tablename__ = 'poems'

    id = Column(String(100), primary_key=True, default=generate_uuid)
    author_id = Column(String(100), ForeignKey("authors.id"))
    title = Column(String(255))
    poem = Column(Text)
    translator_firstname = Column(String(255))
    translator_lastname = Column(String(255))
    isbn = Column(String(50))

    authors = relationship("Author", back_populates="poems")

class User(Base):
    __tablename__ = 'users'

    id = Column(String(255), primary_key=True, default=generate_uuid)
    username = Column(String(50), nullable=False)
    password = Column(String(255), nullable=False)