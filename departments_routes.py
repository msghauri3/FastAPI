from fastapi import APIRouter, HTTPException
from typing import List
import pyodbc
from database import get_db_connection
from departments_models import Department, DepartmentCreate, DepartmentUpdate

router = APIRouter(prefix="/departments", tags=["Departments"])

# ---------------- Create ----------------
@router.post("/", response_model=Department)
async def create_department(department: DepartmentCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = "INSERT INTO dbo.Departments (DepartmentName) VALUES (?)"
        cursor.execute(query, department.DepartmentName)
        conn.commit()

        cursor.execute("SELECT * FROM dbo.Departments WHERE DepartmentID = @@IDENTITY")
        row = cursor.fetchone()
        if row:
            return dict(zip([column[0] for column in cursor.description], row))
        else:
            raise HTTPException(status_code=500, detail="Failed to create department")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

# ---------------- Read all ----------------
@router.get("/", response_model=List[Department])
async def get_all_departments(skip: int = 0, limit: int = 100):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(f"""
            SELECT * FROM dbo.Departments
            ORDER BY DepartmentID
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
@router.get("/{department_id}", response_model=Department)
async def get_department(department_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM dbo.Departments WHERE DepartmentID = ?", department_id)
        row = cursor.fetchone()
        if row:
            return dict(zip([column[0] for column in cursor.description], row))
        else:
            raise HTTPException(status_code=404, detail="Department not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

# ---------------- Update ----------------
@router.put("/{department_id}", response_model=Department)
async def update_department(department_id: int, department: DepartmentUpdate):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT DepartmentID FROM dbo.Departments WHERE DepartmentID = ?", department_id)
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Department not found")

        update_fields = []
        params = []

        if department.DepartmentName is not None:
            update_fields.append("DepartmentName = ?")
            params.append(department.DepartmentName)

        if not update_fields:
            raise HTTPException(status_code=400, detail="No fields to update")

        params.append(department_id)
        query = f"UPDATE dbo.Departments SET {', '.join(update_fields)} WHERE DepartmentID = ?"
        cursor.execute(query, params)
        conn.commit()

        cursor.execute("SELECT * FROM dbo.Departments WHERE DepartmentID = ?", department_id)
        row = cursor.fetchone()
        if row:
            return dict(zip([column[0] for column in cursor.description], row))
        else:
            raise HTTPException(status_code=404, detail="Department not found after update")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

# ---------------- Delete ----------------
@router.delete("/{department_id}")
async def delete_department(department_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM dbo.Departments WHERE DepartmentID = ?", department_id)
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Department not found")
        return {"message": "Department deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()
