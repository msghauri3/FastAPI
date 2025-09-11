from fastapi import APIRouter, HTTPException
from typing import List
import pyodbc
from database import get_db_connection
from user_models import User, UserCreate, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])

# ✅ Create
@router.post("/", response_model=User)
async def create_user(user: UserCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
        INSERT INTO Users (Username, PasswordHash, Role)
        VALUES (?, ?, ?)
        """
        cursor.execute(query, (
            user.Username, user.PasswordHash, user.Role
        ))
        conn.commit()

        cursor.execute("SELECT * FROM Users WHERE uid = @@IDENTITY")
        row = cursor.fetchone()
        if row:
            return dict(zip([column[0] for column in cursor.description], row))
        else:
            raise HTTPException(status_code=500, detail="Failed to create user")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()


# ✅ Read All
@router.get("/", response_model=List[User])
async def get_all_users(skip: int = 0, limit: int = 100):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT * FROM Users ORDER BY uid OFFSET {skip} ROWS FETCH NEXT {limit} ROWS ONLY")
        rows = cursor.fetchall()
        return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()


# ✅ Read One
@router.get("/{uid}", response_model=User)
async def get_user(uid: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Users WHERE uid = ?", uid)
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
@router.put("/{uid}", response_model=User)
async def update_user(uid: int, user: UserUpdate):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT uid FROM Users WHERE uid = ?", uid)
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="User not found")

        update_fields = []
        params = []

        if user.Username is not None:
            update_fields.append("Username = ?")
            params.append(user.Username)
        if user.PasswordHash is not None:
            update_fields.append("PasswordHash = ?")
            params.append(user.PasswordHash)
        if user.Role is not None:
            update_fields.append("Role = ?")
            params.append(user.Role)

        if not update_fields:
            raise HTTPException(status_code=400, detail="No fields to update")

        params.append(uid)
        query = f"UPDATE Users SET {', '.join(update_fields)} WHERE uid = ?"
        cursor.execute(query, params)
        conn.commit()

        cursor.execute("SELECT * FROM Users WHERE uid = ?", uid)
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
async def delete_user(uid: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Users WHERE uid = ?", uid)
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": "User deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()
