from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import pyodbc
from datetime import datetime
from database import get_db_connection
from models import Employee, EmployeeCreate, EmployeeUpdate

app = FastAPI(title="Employee Management API", version="1.0.0")

# Configure CORS middleware - UPDATED TO FIX THE ISSUE
origins = [
    "http://localhost:3000",      # React local dev
    "http://172.20.228.2:3000",   # If React served via this IP
    "http://localhost:8000",      # Allow same origin
    "http://172.20.228.2:8000",   # Allow same origin
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
    expose_headers=["*"]  # Expose all headers
)

# CRUD Operations (your existing code remains the same)
@app.post("/employees/", response_model=Employee)
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
        
        # Get the created employee
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

@app.get("/employees/", response_model=List[Employee])
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

# ... (keep the rest of your existing endpoints: get_employee, update_employee, delete_employee, root)

# Add this at the end of your main.py file
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host="0.0.0.0",  # Listen on all interfaces
        port=8000,
        reload=False  # Disable reload in production
    )