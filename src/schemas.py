from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from enum import Enum
from datetime import datetime


class Role(Enum):
    admin = 'Administrator'
    moderator = 'Moderator'
    user = 'User'


class UserModel(BaseModel):
    username: str = Field(min_length=3)
    firstname: Optional[str] = Field(min_length=3)
    lastname: Optional[str] = Field(min_length=3)
    email: EmailStr
    password: str = Field(min_length=6)
    role: Optional[Role]
    avatar: Optional[str]


class UserDB(BaseModel):
    id: int
    username: str
    firstname: str | None
    lastname: str | None
    email: EmailStr
    password: str
    role: Role
    avatar: str | None
    created_at: datetime
    update_at: datetime

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    detail: str = 'User successfully created'
    data: UserDB

