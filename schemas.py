from pydantic import BaseModel, ValidationError

# author classes

class AuthorBase(BaseModel):
    firstname: str
    lastname: str | None = None

class AuthorCreate(AuthorBase):
    pass

class Author(AuthorBase):
    id: str

    class Config:
        from_attributes = True

class AuthorUpdate(AuthorBase):
    firstname: str | None = None 
    lastname: str | None = None

# poem classes

class PoemBase(BaseModel):
    id: str
    author_id: str
    title: str | None = None
    poem : str
    translator_firstname: str | None = None
    translator_lastname: str | None = None
    isbn: str | None = None

class PoemUpdate(BaseModel):
    author_id: str | None = None
    title: str | None = None
    poem : str | None = None
    translator_firstname: str | None = None
    translator_lastname: str | None = None
    isbn: str | None = None

class Poem(BaseModel):
    id: str
    author_id: str
    title: str | None = None
    poem: str

class PoemCreate(BaseModel):
    title: str | None = None
    poem: str

# user classes
    
class UserBase(BaseModel):
    id: str
    username: str
    password: str

class User(BaseModel):
    username: str
    password: str

class UserCreate(User):
    pass

class UserInfo(BaseModel):
    id: str
    username: str

class UserUsername(BaseModel):
    username: str

# security classes 
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
    scopes: list[str] = []