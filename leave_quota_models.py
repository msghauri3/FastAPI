from pydantic import BaseModel
from typing import Optional

class LeaveQuotaBase(BaseModel):
    LeaveTypeName: str
    TotalLeaves: int
    Year: str

class LeaveQuotaCreate(LeaveQuotaBase):
    pass

class LeaveQuotaUpdate(BaseModel):
    LeaveTypeName: Optional[str] = None
    TotalLeaves: Optional[int] = None
    Year: Optional[str] = None

class LeaveQuota(LeaveQuotaBase):
    UID: int   # ✅ Primary Key

    class Config:
        from_attributes = True
