from fastapi import APIRouter, HTTPException
from typing import List
import pyodbc
from database import get_db_connection
from taxslab_models import TaxSlab, TaxSlabCreate, TaxSlabUpdate

router = APIRouter(prefix="/taxslabs", tags=["TaxSlabs"])

# ✅ Create
@router.post("/", response_model=TaxSlab)
async def create_taxslab(taxslab: TaxSlabCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
        INSERT INTO TaxSlabs (FiscalYearStart, FiscalYearEnd, LowerLimit, UpperLimit, TaxRate)
        VALUES (?, ?, ?, ?, ?)
        """
        cursor.execute(query, (
            taxslab.FiscalYearStart, taxslab.FiscalYearEnd,
            taxslab.LowerLimit, taxslab.UpperLimit, taxslab.TaxRate
        ))
        conn.commit()

        cursor.execute("SELECT * FROM TaxSlabs WHERE SlabID = @@IDENTITY")
        row = cursor.fetchone()
        if row:
            return dict(zip([column[0] for column in cursor.description], row))
        else:
            raise HTTPException(status_code=500, detail="Failed to create tax slab")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()


# ✅ Read All
@router.get("/", response_model=List[TaxSlab])
async def get_all_taxslabs(skip: int = 0, limit: int = 100):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT * FROM TaxSlabs ORDER BY SlabID OFFSET {skip} ROWS FETCH NEXT {limit} ROWS ONLY")
        rows = cursor.fetchall()
        return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()


# ✅ Read One
@router.get("/{slab_id}", response_model=TaxSlab)
async def get_taxslab(slab_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM TaxSlabs WHERE SlabID = ?", slab_id)
        row = cursor.fetchone()
        if row:
            return dict(zip([column[0] for column in cursor.description], row))
        else:
            raise HTTPException(status_code=404, detail="Tax slab not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()


# ✅ Update
@router.put("/{slab_id}", response_model=TaxSlab)
async def update_taxslab(slab_id: int, taxslab: TaxSlabUpdate):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT SlabID FROM TaxSlabs WHERE SlabID = ?", slab_id)
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Tax slab not found")

        update_fields = []
        params = []

        if taxslab.FiscalYearStart is not None:
            update_fields.append("FiscalYearStart = ?")
            params.append(taxslab.FiscalYearStart)
        if taxslab.FiscalYearEnd is not None:
            update_fields.append("FiscalYearEnd = ?")
            params.append(taxslab.FiscalYearEnd)
        if taxslab.LowerLimit is not None:
            update_fields.append("LowerLimit = ?")
            params.append(taxslab.LowerLimit)
        if taxslab.UpperLimit is not None:
            update_fields.append("UpperLimit = ?")
            params.append(taxslab.UpperLimit)
        if taxslab.TaxRate is not None:
            update_fields.append("TaxRate = ?")
            params.append(taxslab.TaxRate)

        if not update_fields:
            raise HTTPException(status_code=400, detail="No fields to update")

        params.append(slab_id)
        query = f"UPDATE TaxSlabs SET {', '.join(update_fields)} WHERE SlabID = ?"
        cursor.execute(query, params)
        conn.commit()

        cursor.execute("SELECT * FROM TaxSlabs WHERE SlabID = ?", slab_id)
        row = cursor.fetchone()
        if row:
            return dict(zip([column[0] for column in cursor.description], row))
        else:
            raise HTTPException(status_code=404, detail="Tax slab not found after update")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()


# ✅ Delete
@router.delete("/{slab_id}")
async def delete_taxslab(slab_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM TaxSlabs WHERE SlabID = ?", slab_id)
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Tax slab not found")
        return {"message": "Tax slab deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()
