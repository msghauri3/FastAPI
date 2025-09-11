from fastapi import APIRouter, HTTPException
from typing import List
import pyodbc
from datetime import datetime
from database import get_db_connection
from allowance_models import Allowance, AllowanceCreate, AllowanceUpdate

router = APIRouter(prefix="/allowances", tags=["Allowances"])

# ---------------- Create ----------------
@router.post("/", response_model=Allowance)
async def create_allowance(allowance: AllowanceCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
        INSERT INTO dbo.Allowances (EmployeeID, AllowanceType, Amount, IsActive, Frequency)
        VALUES (?, ?, ?, ?, ?)
        """
        cursor.execute(query, (
            allowance.EmployeeID,
            allowance.AllowanceType,
            allowance.Amount,
            allowance.IsActive,
            allowance.Frequency
        ))
        conn.commit()

        cursor.execute("SELECT * FROM dbo.Allowances WHERE AllowanceID = @@IDENTITY")
        row = cursor.fetchone()

        if row:
            return dict(zip([column[0] for column in cursor.description], row))
        else:
            raise HTTPException(status_code=500, detail="Failed to create allowance")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

# ---------------- Read all ----------------
@router.get("/", response_model=List[Allowance])
async def get_all_allowances(skip: int = 0, limit: int = 100):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(f"""
            SELECT * FROM dbo.Allowances
            ORDER BY AllowanceID
            OFFSET {skip} ROWS FETCH NEXT {limit} ROWS ONLY
        """)
        rows = cursor.fetchall()
        return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

# ---------------- Read single ----------------
@router.get("/{allowance_id}", response_model=Allowance)
async def get_allowance(allowance_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM dbo.Allowances WHERE AllowanceID = ?", allowance_id)
        row = cursor.fetchone()
        if row:
            return dict(zip([column[0] for column in cursor.description], row))
        else:
            raise HTTPException(status_code=404, detail="Allowance not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

# ---------------- Update ----------------
@router.put("/{allowance_id}", response_model=Allowance)
async def update_allowance(allowance_id: int, allowance: AllowanceUpdate):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT AllowanceID FROM dbo.Allowances WHERE AllowanceID = ?", allowance_id)
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Allowance not found")

        update_fields = []
        params = []

        if allowance.EmployeeID is not None:
            update_fields.append("EmployeeID = ?")
            params.append(allowance.EmployeeID)
        if allowance.AllowanceType is not None:
            update_fields.append("AllowanceType = ?")
            params.append(allowance.AllowanceType)
        if allowance.Amount is not None:
            update_fields.append("Amount = ?")
            params.append(allowance.Amount)
        if allowance.IsActive is not None:
            update_fields.append("IsActive = ?")
            params.append(allowance.IsActive)
        if allowance.Frequency is not None:
            update_fields.append("Frequency = ?")
            params.append(allowance.Frequency)

        if not update_fields:
            raise HTTPException(status_code=400, detail="No fields to update")

        params.append(allowance_id)
        query = f"UPDATE dbo.Allowances SET {', '.join(update_fields)} WHERE AllowanceID = ?"
        cursor.execute(query, params)
        conn.commit()

        cursor.execute("SELECT * FROM dbo.Allowances WHERE AllowanceID = ?", allowance_id)
        row = cursor.fetchone()
        if row:
            return dict(zip([column[0] for column in cursor.description], row))
        else:
            raise HTTPException(status_code=404, detail="Allowance not found after update")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

# ---------------- Delete ----------------
@router.delete("/{allowance_id}")
async def delete_allowance(allowance_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM dbo.Allowances WHERE AllowanceID = ?", allowance_id)
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Allowance not found")
        return {"message": "Allowance deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()
