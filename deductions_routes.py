from fastapi import APIRouter, HTTPException
from typing import List
import pyodbc
from database import get_db_connection
from deductions_models import Deduction, DeductionCreate, DeductionUpdate

router = APIRouter(prefix="/deductions", tags=["Deductions"])

# ---------------- Create ----------------
@router.post("/", response_model=Deduction)
async def create_deduction(deduction: DeductionCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
        INSERT INTO dbo.Deductions (EmployeeID, DeductionType, Amount, IsActive, Frequency)
        VALUES (?, ?, ?, ?, ?)
        """
        cursor.execute(query, (
            deduction.EmployeeID,
            deduction.DeductionType,
            deduction.Amount,
            deduction.IsActive,
            deduction.Frequency
        ))
        conn.commit()

        cursor.execute("SELECT * FROM dbo.Deductions WHERE DeductionID = @@IDENTITY")
        row = cursor.fetchone()

        if row:
            return dict(zip([column[0] for column in cursor.description], row))
        else:
            raise HTTPException(status_code=500, detail="Failed to create deduction")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

# ---------------- Read all ----------------
@router.get("/", response_model=List[Deduction])
async def get_all_deductions(skip: int = 0, limit: int = 100):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(f"""
            SELECT * FROM dbo.Deductions
            ORDER BY DeductionID
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
@router.get("/{deduction_id}", response_model=Deduction)
async def get_deduction(deduction_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM dbo.Deductions WHERE DeductionID = ?", deduction_id)
        row = cursor.fetchone()
        if row:
            return dict(zip([column[0] for column in cursor.description], row))
        else:
            raise HTTPException(status_code=404, detail="Deduction not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

# ---------------- Update ----------------
@router.put("/{deduction_id}", response_model=Deduction)
async def update_deduction(deduction_id: int, deduction: DeductionUpdate):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT DeductionID FROM dbo.Deductions WHERE DeductionID = ?", deduction_id)
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Deduction not found")

        update_fields = []
        params = []

        if deduction.EmployeeID is not None:
            update_fields.append("EmployeeID = ?")
            params.append(deduction.EmployeeID)
        if deduction.DeductionType is not None:
            update_fields.append("DeductionType = ?")
            params.append(deduction.DeductionType)
        if deduction.Amount is not None:
            update_fields.append("Amount = ?")
            params.append(deduction.Amount)
        if deduction.IsActive is not None:
            update_fields.append("IsActive = ?")
            params.append(deduction.IsActive)
        if deduction.Frequency is not None:
            update_fields.append("Frequency = ?")
            params.append(deduction.Frequency)

        if not update_fields:
            raise HTTPException(status_code=400, detail="No fields to update")

        params.append(deduction_id)
        query = f"UPDATE dbo.Deductions SET {', '.join(update_fields)} WHERE DeductionID = ?"
        cursor.execute(query, params)
        conn.commit()

        cursor.execute("SELECT * FROM dbo.Deductions WHERE DeductionID = ?", deduction_id)
        row = cursor.fetchone()
        if row:
            return dict(zip([column[0] for column in cursor.description], row))
        else:
            raise HTTPException(status_code=404, detail="Deduction not found after update")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

# ---------------- Delete ----------------
@router.delete("/{deduction_id}")
async def delete_deduction(deduction_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM dbo.Deductions WHERE DeductionID = ?", deduction_id)
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Deduction not found")
        return {"message": "Deduction deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()
