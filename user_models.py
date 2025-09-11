from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    Username: Optional[str] = None
    PasswordHash: str
    Role: str

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    Username: Optional[str] = None
    PasswordHash: Optional[str] = None
    Role: Optional[str] = None

class User(UserBase):
    uid: int

    class Config:
        from_attributes = True
