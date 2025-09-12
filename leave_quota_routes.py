from fastapi import APIRouter, HTTPException
from typing import List
import pyodbc
from database import get_db_connection
from leave_quota_models import LeaveQuota, LeaveQuotaCreate, LeaveQuotaUpdate

router = APIRouter(prefix="/leave-quota", tags=["LeaveQuota"])

# ✅ Create
@router.post("/", response_model=LeaveQuota)
async def create_quota(quota: LeaveQuotaCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
        INSERT INTO LeaveQuota (LeaveTypeName, TotalLeaves, Year)
        VALUES (?, ?, ?)
        """
        cursor.execute(query, (quota.LeaveTypeName, quota.TotalLeaves, quota.Year))
        conn.commit()

        cursor.execute("SELECT TOP 1 * FROM LeaveQuota ORDER BY UID DESC")
        row = cursor.fetchone()
        if row:
            return dict(zip([column[0] for column in cursor.description], row))
        else:
            raise HTTPException(status_code=500, detail="Failed to insert LeaveQuota")
    finally:
        cursor.close()
        conn.close()

# ✅ Read All
@router.get("/", response_model=List[LeaveQuota])
async def get_all_quotas(skip: int = 0, limit: int = 100):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = "SELECT * FROM LeaveQuota ORDER BY UID OFFSET ? ROWS FETCH NEXT ? ROWS ONLY"
        cursor.execute(query, (skip, limit))
        rows = cursor.fetchall()
        return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]
    finally:
        cursor.close()
        conn.close()

# ✅ Read One
@router.get("/{uid}", response_model=LeaveQuota)
async def get_quota(uid: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM LeaveQuota WHERE UID = ?", uid)
        row = cursor.fetchone()
        if row:
            return dict(zip([column[0] for column in cursor.description], row))
        else:
            raise HTTPException(status_code=404, detail="LeaveQuota not found")
    finally:
        cursor.close()
        conn.close()

# ✅ Update
@router.put("/{uid}", response_model=LeaveQuota)
async def update_quota(uid: int, quota: LeaveQuotaUpdate):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        fields = quota.dict(exclude_unset=True)
        if not fields:
            raise HTTPException(status_code=400, detail="No fields to update")

        update_fields = ", ".join([f"{key} = ?" for key in fields.keys()])
        params = list(fields.values())
        params.append(uid)

        query = f"UPDATE LeaveQuota SET {update_fields} WHERE UID = ?"
        cursor.execute(query, params)
        conn.commit()

        cursor.execute("SELECT * FROM LeaveQuota WHERE UID = ?", uid)
        row = cursor.fetchone()
        if row:
            return dict(zip([column[0] for column in cursor.description], row))
        else:
            raise HTTPException(status_code=404, detail="LeaveQuota not found after update")
    finally:
        cursor.close()
        conn.close()

# ✅ Delete
@router.delete("/{uid}")
async def delete_quota(uid: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM LeaveQuota WHERE UID = ?", uid)
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="LeaveQuota not found")
        return {"message": "LeaveQuota deleted successfully"}
    finally:
        cursor.close()
        conn.close()
