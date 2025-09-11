from fastapi import APIRouter, HTTPException
from typing import List
import pyodbc
from database import get_db_connection
from salary_payment_models import SalaryPayment, SalaryPaymentCreate, SalaryPaymentUpdate

router = APIRouter(prefix="/salary-payments", tags=["Salary Payments"])

# Create
@router.post("/", response_model=SalaryPayment)
async def create_salary_payment(payment: SalaryPaymentCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
        INSERT INTO dbo.SalaryPayments
        (EmployeeID, SalaryYear, SalaryMonth, BasicSalary, TotalAllowances, 
         TotalDeductions, TaxAmount, PaymentDate, SlabID, GrossSalary)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(query, (
            payment.EmployeeID,
            payment.SalaryYear,
            payment.SalaryMonth,
            payment.BasicSalary,
            payment.TotalAllowances,
            payment.TotalDeductions,
            payment.TaxAmount,
            payment.PaymentDate,
            payment.SlabID,
            payment.GrossSalary
        ))
        conn.commit()

        cursor.execute("SELECT TOP 1 * FROM dbo.SalaryPayments ORDER BY PaymentID DESC")
        row = cursor.fetchone()
        if row:
            return dict(zip([column[0] for column in cursor.description], row))
        raise HTTPException(status_code=500, detail="Failed to create salary payment")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()


# Read all
@router.get("/", response_model=List[SalaryPayment])
async def get_all_salary_payments(skip: int = 0, limit: int = 100):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(f"""
            SELECT * FROM dbo.SalaryPayments
            ORDER BY PaymentID
            OFFSET {skip} ROWS FETCH NEXT {limit} ROWS ONLY
        """)
        rows = cursor.fetchall()
        return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()


# Read single
@router.get("/{payment_id}", response_model=SalaryPayment)
async def get_salary_payment(payment_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM dbo.SalaryPayments WHERE PaymentID = ?", payment_id)
        row = cursor.fetchone()
        if row:
            return dict(zip([column[0] for column in cursor.description], row))
        raise HTTPException(status_code=404, detail="Salary payment not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()


# Update
@router.put("/{payment_id}", response_model=SalaryPayment)
async def update_salary_payment(payment_id: int, payment: SalaryPaymentUpdate):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT PaymentID FROM dbo.SalaryPayments WHERE PaymentID = ?", payment_id)
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Salary payment not found")

        update_fields = []
        params = []

        for field, value in payment.dict(exclude_unset=True).items():
            update_fields.append(f"{field} = ?")
            params.append(value)

        if not update_fields:
            raise HTTPException(status_code=400, detail="No fields to update")

        params.append(payment_id)
        query = f"UPDATE dbo.SalaryPayments SET {', '.join(update_fields)} WHERE PaymentID = ?"
        cursor.execute(query, params)
        conn.commit()

        cursor.execute("SELECT * FROM dbo.SalaryPayments WHERE PaymentID = ?", payment_id)
        row = cursor.fetchone()
        if row:
            return dict(zip([column[0] for column in cursor.description], row))
        raise HTTPException(status_code=404, detail="Salary payment not found after update")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()


# Delete
@router.delete("/{payment_id}")
async def delete_salary_payment(payment_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM dbo.SalaryPayments WHERE PaymentID = ?", payment_id)
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Salary payment not found")
        return {"message": "Salary payment deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()
