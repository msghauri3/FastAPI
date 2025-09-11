from pydantic import BaseModel
from typing import Optional
from datetime import date

class GazettedHolidayBase(BaseModel):
    Description: Optional[str] = None

class GazettedHolidayCreate(GazettedHolidayBase):
    HolidayDate: date   # ✅ primary key

class GazettedHolidayUpdate(GazettedHolidayBase):
    pass  # sirf Description update hoga

class GazettedHoliday(GazettedHolidayBase):
    HolidayDate: date

    class Config:
        from_attributes = True
