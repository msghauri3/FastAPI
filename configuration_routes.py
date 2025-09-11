from fastapi import APIRouter, HTTPException
from typing import List
import pyodbc
from database import get_db_connection
from configuration_models import Configuration, ConfigurationCreate, ConfigurationUpdate

router = APIRouter(prefix="/configurations", tags=["Configurations"])

# ---------------- Create ----------------
@router.post("/", response_model=Configuration)
async def create_configuration(config: ConfigurationCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
        INSERT INTO dbo.Configuration (ConfigKey, ConfigValue)
        VALUES (?, ?)
        """
        cursor.execute(query, (config.ConfigKey, config.ConfigValue))
        conn.commit()

        cursor.execute("SELECT * FROM dbo.Configuration WHERE UID = @@IDENTITY")
        row = cursor.fetchone()

        if row:
            return dict(zip([column[0] for column in cursor.description], row))
        else:
            raise HTTPException(status_code=500, detail="Failed to create configuration")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

# ---------------- Read all ----------------
@router.get("/", response_model=List[Configuration])
async def get_all_configurations(skip: int = 0, limit: int = 100):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(f"""
            SELECT * FROM dbo.Configuration
            ORDER BY UID
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
@router.get("/{uid}", response_model=Configuration)
async def get_configuration(uid: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM dbo.Configuration WHERE UID = ?", uid)
        row = cursor.fetchone()
        if row:
            return dict(zip([column[0] for column in cursor.description], row))
        else:
            raise HTTPException(status_code=404, detail="Configuration not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

# ---------------- Update ----------------
@router.put("/{uid}", response_model=Configuration)
async def update_configuration(uid: int, config: ConfigurationUpdate):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT UID FROM dbo.Configuration WHERE UID = ?", uid)
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Configuration not found")

        update_fields = []
        params = []

        if config.ConfigKey is not None:
            update_fields.append("ConfigKey = ?")
            params.append(config.ConfigKey)
        if config.ConfigValue is not None:
            update_fields.append("ConfigValue = ?")
            params.append(config.ConfigValue)

        if not update_fields:
            raise HTTPException(status_code=400, detail="No fields to update")

        params.append(uid)
        query = f"UPDATE dbo.Configuration SET {', '.join(update_fields)} WHERE UID = ?"
        cursor.execute(query, params)
        conn.commit()

        cursor.execute("SELECT * FROM dbo.Configuration WHERE UID = ?", uid)
        row = cursor.fetchone()
        if row:
            return dict(zip([column[0] for column in cursor.description], row))
        else:
            raise HTTPException(status_code=404, detail="Configuration not found after update")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

# ---------------- Delete ----------------
@router.delete("/{uid}")
async def delete_configuration(uid: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM dbo.Configuration WHERE UID = ?", uid)
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Configuration not found")
        return {"message": "Configuration deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()
