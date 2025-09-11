from pydantic import BaseModel
from typing import Optional

class DepartmentBase(BaseModel):
    DepartmentName: Optional[str] = None

class DepartmentCreate(DepartmentBase):
    DepartmentName: str

class DepartmentUpdate(DepartmentBase):
    pass

class Department(DepartmentBase):
    DepartmentID: int

    class Config:
        from_attributes = True
