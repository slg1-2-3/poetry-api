from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, Integer
from sqlalchemy.orm import relationship

from database import Base


class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String(100))
    lastname = Column(String(100))

    poems = relationship("Poem", back_populates="authors")

class Poem(Base):
    __tablename__ = 'poems'

    id = Column(Integer, primary_key=True, index=True)
    author_id = Column(Integer, ForeignKey("authors.id"))
    title = Column(String(255))
    poem = Column(Text)
    translator_firstname = Column(String(255))
    translator_lastname = Column(String(255))
    isbn = Column(String(50))

    authors = relationship("Author", back_populates="poems")
