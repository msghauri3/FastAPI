from pydantic import BaseModel
from typing import Optional

class LoginBase(BaseModel):
    UserID: str
    Username: Optional[str] = None
    Password: Optional[str] = None
    Role: Optional[str] = None

class LoginCreate(LoginBase):
    pass

class LoginUpdate(BaseModel):
    Username: Optional[str] = None
    Password: Optional[str] = None
    Role: Optional[str] = None

class Login(LoginBase):
    uid: int

    class Config:
        from_attributes = True
