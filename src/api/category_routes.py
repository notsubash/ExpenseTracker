from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.database.db_connection import conn, cursor
from dotenv import load_dotenv
from psycopg2 import errors


load_dotenv()

router = APIRouter()

class CategoryCreate(BaseModel):
    category_name: str

@router.get("/categories")
def get_categories():
    cursor.execute("SELECT * FROM categories")
    categories = cursor.fetchall()
    if not categories:
        raise HTTPException(status_code=404, detail="No categories found")
    return [{"category_id": c[0], "category_name": c[1]} for c in categories]

@router.post("/categories", status_code=201)
def create_category(category: CategoryCreate):
    try:
        cursor.execute(
            "INSERT INTO CATEGORIES (category_name) VALUES (%s) RETURNING category_id",
            (category.category_name,)
        )
        conn.commit()
        category_id = cursor.fetchone()[0]
        return {"category_id": category_id, "category_name": category.category_name}
    except errors.UniqueViolation:
        conn.rollback()
        raise HTTPException(status_code=400, detail="Category already exists")
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@router.delete("/categories")
def delete_category(category_id: int):
    cursor.execute("DELETE FROM categories WHERE category_id = %s RETURNING category_id",
                    (category_id,)
    )
    result = cursor.fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="Category not found")
    conn.commit()
    return {"message": "Category deleted successfully"}