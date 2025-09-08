from fastapi import APIRouter, HTTPException
from typing import List, Optional
import pyodbc
from datetime import datetime
from database import get_db_connection
from employees_models import Employee, EmployeeCreate, EmployeeUpdate

router = APIRouter(prefix="/employees", tags=["Employees"])

@router.post("/", response_model=Employee)
async def create_employee(employee: EmployeeCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        query = """
        INSERT INTO Employee (
            EmployeeID, EmployeeName, CNIC, FatherName, DOB, MobileNo, 
            Department, Designation, DateOfJoining, EmployeeStatus, 
            ModifiedBy, ModifiedOn, Details, Project, CarryForwardLeaves, 
            Year2022, Year2023, AdjustedAjusted, Year2024, CarryForwardLeaves1, 
            Year2023New, BasicSalary, ApplyTax
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        cursor.execute(query, (
            employee.EmployeeID, employee.EmployeeName, employee.CNIC, 
            employee.FatherName, employee.DOB, employee.MobileNo, 
            employee.Department, employee.Designation, employee.DateOfJoining, 
            employee.EmployeeStatus, employee.ModifiedBy, employee.ModifiedOn, 
            employee.Details, employee.Project, employee.CarryForwardLeaves, 
            employee.Year2022, employee.Year2023, employee.AdjustedAjusted, 
            employee.Year2024, employee.CarryForwardLeaves1, employee.Year2023New, 
            employee.BasicSalary, employee.ApplyTax
        ))
        
        conn.commit()
        
        cursor.execute("SELECT * FROM Employee WHERE uid = @@IDENTITY")
        row = cursor.fetchone()
        
        if row:
            return dict(zip([column[0] for column in cursor.description], row))
        else:
            raise HTTPException(status_code=500, detail="Failed to create employee")
            
    except pyodbc.IntegrityError as e:
        if "UQ__Employee" in str(e):
            raise HTTPException(status_code=400, detail="EmployeeID already exists")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.get("/", response_model=List[Employee])
async def get_all_employees(skip: int = 0, limit: int = 100):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(f"SELECT * FROM Employee ORDER BY uid OFFSET {skip} ROWS FETCH NEXT {limit} ROWS ONLY")
        rows = cursor.fetchall()
        
        employees = []
        for row in rows:
            employees.append(dict(zip([column[0] for column in cursor.description], row)))
        
        return employees
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.get("/{employee_id}", response_model=Employee)
async def get_employee(employee_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT * FROM Employee WHERE EmployeeID = ?", employee_id)
        row = cursor.fetchone()
        
        if row:
            return dict(zip([column[0] for column in cursor.description], row))
        else:
            raise HTTPException(status_code=404, detail="Employee not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.put("/{employee_id}", response_model=Employee)
async def update_employee(employee_id: str, employee: EmployeeUpdate):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT uid FROM Employee WHERE EmployeeID = ?", employee_id)
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Employee not found")
        
        update_fields = []
        params = []
        
        if employee.EmployeeName is not None:
            update_fields.append("EmployeeName = ?")
            params.append(employee.EmployeeName)
        if employee.CNIC is not None:
            update_fields.append("CNIC = ?")
            params.append(employee.CNIC)
        if employee.FatherName is not None:
            update_fields.append("FatherName = ?")
            params.append(employee.FatherName)
        if employee.DOB is not None:
            update_fields.append("DOB = ?")
            params.append(employee.DOB)
        if employee.MobileNo is not None:
            update_fields.append("MobileNo = ?")
            params.append(employee.MobileNo)
        if employee.Department is not None:
            update_fields.append("Department = ?")
            params.append(employee.Department)
        if employee.Designation is not None:
            update_fields.append("Designation = ?")
            params.append(employee.Designation)
        if employee.DateOfJoining is not None:
            update_fields.append("DateOfJoining = ?")
            params.append(employee.DateOfJoining)
        if employee.EmployeeStatus is not None:
            update_fields.append("EmployeeStatus = ?")
            params.append(employee.EmployeeStatus)
        if employee.ModifiedBy is not None:
            update_fields.append("ModifiedBy = ?")
            params.append(employee.ModifiedBy)
        if employee.ModifiedOn is not None:
            update_fields.append("ModifiedOn = ?")
            params.append(employee.ModifiedOn)
        if employee.Details is not None:
            update_fields.append("Details = ?")
            params.append(employee.Details)
        if employee.Project is not None:
            update_fields.append("Project = ?")
            params.append(employee.Project)
        if employee.CarryForwardLeaves is not None:
            update_fields.append("CarryForwardLeaves = ?")
            params.append(employee.CarryForwardLeaves)
        if employee.Year2022 is not None:
            update_fields.append("Year2022 = ?")
            params.append(employee.Year2022)
        if employee.Year2023 is not None:
            update_fields.append("Year2023 = ?")
            params.append(employee.Year2023)
        if employee.AdjustedAjusted is not None:
            update_fields.append("AdjustedAjusted = ?")
            params.append(employee.AdjustedAjusted)
        if employee.Year2024 is not None:
            update_fields.append("Year2024 = ?")
            params.append(employee.Year2024)
        if employee.CarryForwardLeaves1 is not None:
            update_fields.append("CarryForwardLeaves1 = ?")
            params.append(employee.CarryForwardLeaves1)
        if employee.Year2023New is not None:
            update_fields.append("Year2023New = ?")
            params.append(employee.Year2023New)
        if employee.BasicSalary is not None:
            update_fields.append("BasicSalary = ?")
            params.append(employee.BasicSalary)
        if employee.ApplyTax is not None:
            update_fields.append("ApplyTax = ?")
            params.append(employee.ApplyTax)
        
        if not update_fields:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        update_fields.append("ModifiedOn = ?")
        params.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        params.append(employee_id)
        
        query = f"UPDATE Employee SET {', '.join(update_fields)} WHERE EmployeeID = ?"
        cursor.execute(query, params)
        conn.commit()
        
        cursor.execute("SELECT * FROM Employee WHERE EmployeeID = ?", employee_id)
        row = cursor.fetchone()
        
        if row:
            return dict(zip([column[0] for column in cursor.description], row))
        else:
            raise HTTPException(status_code=404, detail="Employee not found after update")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.delete("/{employee_id}")
async def delete_employee(employee_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("DELETE FROM Employee WHERE EmployeeID = ?", employee_id)
        conn.commit()
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Employee not found")
        
        return {"message": "Employee deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()