from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


# create a class and make a template for the user and bound him/her. Use the pydantic lib "All this is for validation purpose".


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    owner_id: int
    created_at: datetime 

    class Config:
        orm_mode = True

class UsersCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime 

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None