from fastapi import APIRouter, HTTPException
from typing import List
import pyodbc
from database import get_db_connection
from promotion_models import Promotion, PromotionCreate, PromotionUpdate

router = APIRouter(prefix="/promotions", tags=["Promotions"])

# ✅ Create
@router.post("/", response_model=Promotion)
async def create_promotion(promotion: PromotionCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
        INSERT INTO Promotions (EmployeeID, Title, EffectiveDate, NewSalary, Remarks)
        VALUES (?, ?, ?, ?, ?)
        """
        cursor.execute(query, (
            promotion.EmployeeID,
            promotion.Title,
            promotion.EffectiveDate,
            promotion.NewSalary,
            promotion.Remarks
        ))
        conn.commit()

        cursor.execute("SELECT TOP 1 * FROM Promotions ORDER BY PromotionID DESC")
        row = cursor.fetchone()
        if row:
            return dict(zip([column[0] for column in cursor.description], row))
        raise HTTPException(status_code=500, detail="Failed to insert promotion")
    finally:
        cursor.close()
        conn.close()

# ✅ Read All
@router.get("/", response_model=List[Promotion])
async def get_all_promotions(skip: int = 0, limit: int = 100):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = "SELECT * FROM Promotions ORDER BY PromotionID OFFSET ? ROWS FETCH NEXT ? ROWS ONLY"
        cursor.execute(query, (skip, limit))
        rows = cursor.fetchall()
        return [dict(zip([column[0] for column in cursor.description], row)) for row in rows]
    finally:
        cursor.close()
        conn.close()

# ✅ Read One
@router.get("/{promotion_id}", response_model=Promotion)
async def get_promotion(promotion_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM Promotions WHERE PromotionID = ?", promotion_id)
        row = cursor.fetchone()
        if row:
            return dict(zip([column[0] for column in cursor.description], row))
        raise HTTPException(status_code=404, detail="Promotion not found")
    finally:
        cursor.close()
        conn.close()

# ✅ Update
@router.put("/{promotion_id}", response_model=Promotion)
async def update_promotion(promotion_id: int, promotion: PromotionUpdate):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        fields = promotion.dict(exclude_unset=True)
        if not fields:
            raise HTTPException(status_code=400, detail="No fields to update")

        update_fields = ", ".join([f"{key} = ?" for key in fields.keys()])
        params = list(fields.values())
        params.append(promotion_id)

        query = f"UPDATE Promotions SET {update_fields} WHERE PromotionID = ?"
        cursor.execute(query, params)
        conn.commit()

        cursor.execute("SELECT * FROM Promotions WHERE PromotionID = ?", promotion_id)
        row = cursor.fetchone()
        if row:
            return dict(zip([column[0] for column in cursor.description], row))
        raise HTTPException(status_code=404, detail="Promotion not found after update")
    finally:
        cursor.close()
        conn.close()

# ✅ Delete
@router.delete("/{promotion_id}")
async def delete_promotion(promotion_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Promotions WHERE PromotionID = ?", promotion_id)
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Promotion not found")
        return {"message": "Promotion deleted successfully"}
    finally:
        cursor.close()
        conn.close()
