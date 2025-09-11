from fastapi import APIRouter, HTTPException
from typing import List
import pyodbc
from database import get_db_connection
from login_models import Login, LoginCreate, LoginUpdate

router = APIRouter(prefix="/logins", tags=["Logins"])

# ✅ Create
@router.post("/", response_model=Login)
async def create_login(user: LoginCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
        INSERT INTO Tbl_login (UserID, Username, Password, Role)
        VALUES (?, ?, ?, ?)
        """
        cursor.execute(query, (
            user.UserID, user.Username, user.Password, user.Role
        ))
        conn.commit()

        cursor.execute("SELECT * FROM Tbl_login WHERE uid = @@IDENTITY")
        row = cursor.fetchone()
        if row:
            return dict(zip([column[0] for column in cursor.description], row))
        else:
            raise HTTPException(status_code=500, detail="Failed to create login user")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()


# ✅ Read All
@router.get("/", response_model=List[Login])
async def get_all_logins(skip: int = 0, limit: int = 100):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT * FROM Tbl_login ORDER BY uid OFFSET {skip} ROWS FETCH NEXT {limit} ROWS ONLY")
        rows = cursor.fetchall()
        return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()


# ✅ Read One
@router.get("/{uid}", response_model=Login)
async def get_login(uid: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Tbl_login WHERE uid = ?", uid)
        row = cursor.fetchone()
        if row:
            return dict(zip([column[0] for column in cursor.description], row))
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()


# ✅ Update
@router.put("/{uid}", response_model=Login)
async def update_login(uid: int, user: LoginUpdate):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT uid FROM Tbl_login WHERE uid = ?", uid)
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="User not found")

        update_fields = []
        params = []

        if user.Username is not None:
            update_fields.append("Username = ?")
            params.append(user.Username)
        if user.Password is not None:
            update_fields.append("Password = ?")
            params.append(user.Password)
        if user.Role is not None:
            update_fields.append("Role = ?")
            params.append(user.Role)

        if not update_fields:
            raise HTTPException(status_code=400, detail="No fields to update")

        params.append(uid)
        query = f"UPDATE Tbl_login SET {', '.join(update_fields)} WHERE uid = ?"
        cursor.execute(query, params)
        conn.commit()

        cursor.execute("SELECT * FROM Tbl_login WHERE uid = ?", uid)
        row = cursor.fetchone()
        if row:
            return dict(zip([column[0] for column in cursor.description], row))
        else:
            raise HTTPException(status_code=404, detail="User not found after update")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()


# ✅ Delete
@router.delete("/{uid}")
async def delete_login(uid: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Tbl_login WHERE uid = ?", uid)
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": "User deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()
