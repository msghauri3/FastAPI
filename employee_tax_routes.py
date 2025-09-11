from fastapi import APIRouter, HTTPException
from typing import List
import pyodbc
from database import get_db_connection
from employee_tax_models import EmployeeTax, EmployeeTaxCreate, EmployeeTaxUpdate

router = APIRouter(prefix="/employee-tax", tags=["EmployeeTax"])

# ✅ Create
@router.post("/", response_model=EmployeeTax)
async def create_tax_record(tax: EmployeeTaxCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
        INSERT INTO EmployeeTax (EmployeeID, SalaryYear, SalaryMonth, SlabID, TaxAmount)
        VALUES (?, ?, ?, ?, ?)
        """
        cursor.execute(query, (
            tax.EmployeeID, tax.SalaryYear, tax.SalaryMonth, tax.SlabID, tax.TaxAmount
        ))
        conn.commit()

        # Last inserted row fetch karein
        cursor.execute("SELECT TOP 1 * FROM EmployeeTax ORDER BY TaxID DESC")
        row = cursor.fetchone()
        if row:
            return dict(zip([column[0] for column in cursor.description], row))
        else:
            raise HTTPException(status_code=500, detail="Failed to create record")
    finally:
        cursor.close()
        conn.close()

# ✅ Read All
@router.get("/", response_model=List[EmployeeTax])
async def get_all_tax_records(skip: int = 0, limit: int = 100):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = "SELECT * FROM EmployeeTax ORDER BY TaxID OFFSET ? ROWS FETCH NEXT ? ROWS ONLY"
        cursor.execute(query, (skip, limit))
        rows = cursor.fetchall()
        return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]
    finally:
        cursor.close()
        conn.close()

# ✅ Read One
@router.get("/{tax_id}", response_model=EmployeeTax)
async def get_tax_record(tax_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM EmployeeTax WHERE TaxID = ?", tax_id)
        row = cursor.fetchone()
        if row:
            return dict(zip([column[0] for column in cursor.description], row))
        else:
            raise HTTPException(status_code=404, detail="Tax record not found")
    finally:
        cursor.close()
        conn.close()

# ✅ Update
@router.put("/{tax_id}", response_model=EmployeeTax)
async def update_tax_record(tax_id: int, tax: EmployeeTaxUpdate):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        fields = tax.dict(exclude_unset=True)
        if not fields:
            raise HTTPException(status_code=400, detail="No fields to update")

        update_fields = ", ".join([f"{key} = ?" for key in fields.keys()])
        params = list(fields.values())
        params.append(tax_id)

        query = f"UPDATE EmployeeTax SET {update_fields} WHERE TaxID = ?"
        cursor.execute(query, params)
        conn.commit()

        cursor.execute("SELECT * FROM EmployeeTax WHERE TaxID = ?", tax_id)
        row = cursor.fetchone()
        if row:
            return dict(zip([column[0] for column in cursor.description], row))
        else:
            raise HTTPException(status_code=404, detail="Record not found after update")
    finally:
        cursor.close()
        conn.close()

# ✅ Delete
@router.delete("/{tax_id}")
async def delete_tax_record(tax_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM EmployeeTax WHERE TaxID = ?", tax_id)
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Tax record not found")
        return {"message": "Tax record deleted successfully"}
    finally:
        cursor.close()
        conn.close()
