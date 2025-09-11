from fastapi import APIRouter, HTTPException
from typing import List
import pyodbc
from database import get_db_connection
from employee_leave_summary_models import (
    EmployeeLeaveSummary, EmployeeLeaveSummaryCreate, EmployeeLeaveSummaryUpdate
)

router = APIRouter(prefix="/leave-summary", tags=["EmployeeLeaveSummary"])

# ✅ Create
@router.post("/", response_model=EmployeeLeaveSummary)
async def create_leave_summary(summary: EmployeeLeaveSummaryCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
        INSERT INTO EmployeeLeaveSummary2024 (
            EmployeeID, TotalYear2022, RemainingYear2022, 
            TotalYear2023, RemainingYear2023, 
            TotalYear2024, RemainingYear2024,
            TotalAllYears, RemainingAllYears
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(query, (
            summary.EmployeeID, summary.TotalYear2022, summary.RemainingYear2022,
            summary.TotalYear2023, summary.RemainingYear2023,
            summary.TotalYear2024, summary.RemainingYear2024,
            summary.TotalAllYears, summary.RemainingAllYears
        ))
        conn.commit()

        cursor.execute("SELECT TOP 1 * FROM EmployeeLeaveSummary2024 WHERE EmployeeID = ? ORDER BY EmployeeID DESC", summary.EmployeeID)
        row = cursor.fetchone()
        if row:
            return dict(zip([column[0] for column in cursor.description], row))
        else:
            raise HTTPException(status_code=500, detail="Failed to create record")
    finally:
        cursor.close()
        conn.close()

# ✅ Read All
@router.get("/", response_model=List[EmployeeLeaveSummary])
async def get_all_leave_summaries(skip: int = 0, limit: int = 100):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = "SELECT * FROM EmployeeLeaveSummary2024 ORDER BY EmployeeID OFFSET ? ROWS FETCH NEXT ? ROWS ONLY"
        cursor.execute(query, (skip, limit))
        rows = cursor.fetchall()
        return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]
    finally:
        cursor.close()
        conn.close()

# ✅ Read One
@router.get("/{employee_id}", response_model=EmployeeLeaveSummary)
async def get_leave_summary(employee_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM EmployeeLeaveSummary2024 WHERE EmployeeID = ?", employee_id)
        row = cursor.fetchone()
        if row:
            return dict(zip([column[0] for column in cursor.description], row))
        else:
            raise HTTPException(status_code=404, detail="Record not found")
    finally:
        cursor.close()
        conn.close()

# ✅ Update
@router.put("/{employee_id}", response_model=EmployeeLeaveSummary)
async def update_leave_summary(employee_id: int, summary: EmployeeLeaveSummaryUpdate):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        fields = summary.dict(exclude_unset=True)
        if not fields:
            raise HTTPException(status_code=400, detail="No fields to update")

        update_fields = ", ".join([f"{key} = ?" for key in fields.keys()])
        params = list(fields.values())
        params.append(employee_id)

        query = f"UPDATE EmployeeLeaveSummary2024 SET {update_fields} WHERE EmployeeID = ?"
        cursor.execute(query, params)
        conn.commit()

        cursor.execute("SELECT * FROM EmployeeLeaveSummary2024 WHERE EmployeeID = ?", employee_id)
        row = cursor.fetchone()
        if row:
            return dict(zip([column[0] for column in cursor.description], row))
        else:
            raise HTTPException(status_code=404, detail="Record not found after update")
    finally:
        cursor.close()
        conn.close()

# ✅ Delete
@router.delete("/{employee_id}")
async def delete_leave_summary(employee_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM EmployeeLeaveSummary2024 WHERE EmployeeID = ?", employee_id)
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Record not found")
        return {"message": "Leave summary deleted successfully"}
    finally:
        cursor.close()
        conn.close()
