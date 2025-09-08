from fastapi import APIRouter, HTTPException
from typing import List, Optional
import pyodbc
from datetime import datetime
from database import get_db_connection
from leaves_models import EmployeeLeave, EmployeeLeaveCreate, EmployeeLeaveUpdate

router = APIRouter(prefix="/leaves", tags=["Employee Leaves"])

@router.post("/", response_model=EmployeeLeave)
async def create_employee_leave(leave: EmployeeLeaveCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        query = """
        INSERT INTO EmployeeLeaves (
            EmployeeID, LeaveTypeName, StartDate, EndDate, TotalDays, 
            AddDays, ExcludeDays, Short_Adj, DepSupervisorComments, 
            Year, Status, ApprovedBy, ApprovedOn, AppliedDate
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        cursor.execute(query, (
            leave.EmployeeID, leave.LeaveTypeName, leave.StartDate, leave.EndDate,
            leave.TotalDays, leave.AddDays, leave.ExcludeDays, leave.Short_Adj,
            leave.DepSupervisorComments, leave.Year, leave.Status, leave.ApprovedBy,
            leave.ApprovedOn, leave.AppliedDate
        ))
        
        conn.commit()
        
        cursor.execute("SELECT * FROM EmployeeLeaves WHERE uid = @@IDENTITY")
        row = cursor.fetchone()
        
        if row:
            return dict(zip([column[0] for column in cursor.description], row))
        else:
            raise HTTPException(status_code=500, detail="Failed to create leave record")
            
    except pyodbc.Error as e:
        raise HTTPException(status_code=400, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.get("/", response_model=List[EmployeeLeave])
async def get_all_employee_leaves(
    skip: int = 0, 
    limit: int = 100,
    employee_id: Optional[str] = None,
    status: Optional[str] = None,
    year: Optional[str] = None
):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        base_query = "SELECT * FROM EmployeeLeaves WHERE 1=1"
        params = []
        
        if employee_id:
            base_query += " AND EmployeeID = ?"
            params.append(employee_id)
        
        if status:
            base_query += " AND Status = ?"
            params.append(status)
            
        if year:
            base_query += " AND Year = ?"
            params.append(year)
            
        base_query += f" ORDER BY uid OFFSET {skip} ROWS FETCH NEXT {limit} ROWS ONLY"
        
        cursor.execute(base_query, params)
        rows = cursor.fetchall()
        
        leaves = []
        for row in rows:
            leaves.append(dict(zip([column[0] for column in cursor.description], row)))
        
        return leaves
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.get("/{leave_id}", response_model=EmployeeLeave)
async def get_employee_leave(leave_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT * FROM EmployeeLeaves WHERE uid = ?", leave_id)
        row = cursor.fetchone()
        
        if row:
            return dict(zip([column[0] for column in cursor.description], row))
        else:
            raise HTTPException(status_code=404, detail="Leave record not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.get("/employee/{employee_id}", response_model=List[EmployeeLeave])
async def get_leaves_by_employee(employee_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT * FROM EmployeeLeaves WHERE EmployeeID = ? ORDER BY StartDate DESC", employee_id)
        rows = cursor.fetchall()
        
        leaves = []
        for row in rows:
            leaves.append(dict(zip([column[0] for column in cursor.description], row)))
        
        return leaves
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.put("/{leave_id}", response_model=EmployeeLeave)
async def update_employee_leave(leave_id: int, leave: EmployeeLeaveUpdate):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT uid FROM EmployeeLeaves WHERE uid = ?", leave_id)
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Leave record not found")
        
        update_fields = []
        params = []
        
        if leave.EmployeeID is not None:
            update_fields.append("EmployeeID = ?")
            params.append(leave.EmployeeID)
        if leave.LeaveTypeName is not None:
            update_fields.append("LeaveTypeName = ?")
            params.append(leave.LeaveTypeName)
        if leave.StartDate is not None:
            update_fields.append("StartDate = ?")
            params.append(leave.StartDate)
        if leave.EndDate is not None:
            update_fields.append("EndDate = ?")
            params.append(leave.EndDate)
        if leave.TotalDays is not None:
            update_fields.append("TotalDays = ?")
            params.append(leave.TotalDays)
        if leave.AddDays is not None:
            update_fields.append("AddDays = ?")
            params.append(leave.AddDays)
        if leave.ExcludeDays is not None:
            update_fields.append("ExcludeDays = ?")
            params.append(leave.ExcludeDays)
        if leave.Short_Adj is not None:
            update_fields.append("Short_Adj = ?")
            params.append(leave.Short_Adj)
        if leave.DepSupervisorComments is not None:
            update_fields.append("DepSupervisorComments = ?")
            params.append(leave.DepSupervisorComments)
        if leave.Year is not None:
            update_fields.append("Year = ?")
            params.append(leave.Year)
        if leave.Status is not None:
            update_fields.append("Status = ?")
            params.append(leave.Status)
        if leave.ApprovedBy is not None:
            update_fields.append("ApprovedBy = ?")
            params.append(leave.ApprovedBy)
        if leave.ApprovedOn is not None:
            update_fields.append("ApprovedOn = ?")
            params.append(leave.ApprovedOn)
        if leave.AppliedDate is not None:
            update_fields.append("AppliedDate = ?")
            params.append(leave.AppliedDate)
        
        if not update_fields:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        params.append(leave_id)
        
        query = f"UPDATE EmployeeLeaves SET {', '.join(update_fields)} WHERE uid = ?"
        cursor.execute(query, params)
        conn.commit()
        
        cursor.execute("SELECT * FROM EmployeeLeaves WHERE uid = ?", leave_id)
        row = cursor.fetchone()
        
        if row:
            return dict(zip([column[0] for column in cursor.description], row))
        else:
            raise HTTPException(status_code=404, detail="Leave record not found after update")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.delete("/{leave_id}")
async def delete_employee_leave(leave_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("DELETE FROM EmployeeLeaves WHERE uid = ?", leave_id)
        conn.commit()
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Leave record not found")
        
        return {"message": "Leave record deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.get("/stats/{employee_id}")
async def get_leave_stats(employee_id: str, year: Optional[str] = None):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        base_query = """
        SELECT 
            LeaveTypeName,
            COUNT(*) as TotalLeaves,
            SUM(TotalDays) as TotalDays,
            Status,
            Year
        FROM EmployeeLeaves 
        WHERE EmployeeID = ?
        """
        
        params = [employee_id]
        
        if year:
            base_query += " AND Year = ?"
            params.append(year)
            
        base_query += " GROUP BY LeaveTypeName, Status, Year ORDER BY LeaveTypeName"
        
        cursor.execute(base_query, params)
        rows = cursor.fetchall()
        
        stats = []
        for row in rows:
            stats.append(dict(zip([column[0] for column in cursor.description], row)))
        
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()