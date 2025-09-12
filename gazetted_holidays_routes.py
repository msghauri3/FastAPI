from fastapi import APIRouter, HTTPException
from typing import List
import pyodbc
from database import get_db_connection
from gazetted_holidays_models import GazettedHoliday, GazettedHolidayCreate, GazettedHolidayUpdate

router = APIRouter(prefix="/gazetted-holidays", tags=["GazettedHolidays"])

# ✅ Create
@router.post("/", response_model=GazettedHoliday)
async def create_holiday(holiday: GazettedHolidayCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
        INSERT INTO GazettedHolidays (HolidayDate, Description)
        VALUES (?, ?)
        """
        cursor.execute(query, (holiday.HolidayDate, holiday.Description))
        conn.commit()

        cursor.execute("SELECT * FROM GazettedHolidays WHERE HolidayDate = ?", holiday.HolidayDate)
        row = cursor.fetchone()
        if row:
            return dict(zip([column[0] for column in cursor.description], row))
        else:
            raise HTTPException(status_code=500, detail="Failed to insert holiday")
    finally:
        cursor.close()
        conn.close()

# ✅ Read All
@router.get("/", response_model=List[GazettedHoliday])
async def get_all_holidays(skip: int = 0, limit: int = 100):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = "SELECT * FROM GazettedHolidays ORDER BY HolidayDate OFFSET ? ROWS FETCH NEXT ? ROWS ONLY"
        cursor.execute(query, (skip, limit))
        rows = cursor.fetchall()
        return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]
    finally:
        cursor.close()
        conn.close()

# ✅ Read One
@router.get("/{holiday_date}", response_model=GazettedHoliday)
async def get_holiday(holiday_date: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM GazettedHolidays WHERE HolidayDate = ?", holiday_date)
        row = cursor.fetchone()
        if row:
            return dict(zip([column[0] for column in cursor.description], row))
        else:
            raise HTTPException(status_code=404, detail="Holiday not found")
    finally:
        cursor.close()
        conn.close()

# ✅ Update
@router.put("/{holiday_date}", response_model=GazettedHoliday)
async def update_holiday(holiday_date: str, holiday: GazettedHolidayUpdate):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        fields = holiday.dict(exclude_unset=True)
        if not fields:
            raise HTTPException(status_code=400, detail="No fields to update")

        update_fields = ", ".join([f"{key} = ?" for key in fields.keys()])
        params = list(fields.values())
        params.append(holiday_date)

        query = f"UPDATE GazettedHolidays SET {update_fields} WHERE HolidayDate = ?"
        cursor.execute(query, params)
        conn.commit()

        cursor.execute("SELECT * FROM GazettedHolidays WHERE HolidayDate = ?", holiday_date)
        row = cursor.fetchone()
        if row:
            return dict(zip([column[0] for column in cursor.description], row))
        else:
            raise HTTPException(status_code=404, detail="Holiday not found after update")
    finally:
        cursor.close()
        conn.close()

# ✅ Delete
@router.delete("/{holiday_date}")
async def delete_holiday(holiday_date: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM GazettedHolidays WHERE HolidayDate = ?", holiday_date)
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Holiday not found")
        return {"message": "Holiday deleted successfully"}
    finally:
        cursor.close()
        conn.close()
