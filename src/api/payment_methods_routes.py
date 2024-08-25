from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.database.db_connection import conn, cursor
from dotenv import load_dotenv
from psycopg2 import errors
import logging

logger = logging.getLogger(__name__)

load_dotenv()

router = APIRouter()

class PaymentMethodCreate(BaseModel):
    payment_method_name: str

@router.get("/payment_methods")
def get_payment_methods():
    try:
        cursor.execute("SELECT * FROM payment_methods")
        payment_methods = cursor.fetchall()
        if not payment_methods:
            raise HTTPException(status_code=404, detail="No payment methods found")
        return [{"payment_method_id": p[0], "payment_method_name": p[1]} for p in payment_methods]
    except Exception as e:
        logger.error(f"Error fetching payment methods: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/payment_methods", status_code=201)
def create_payment_method(payment_method: PaymentMethodCreate):
    try:
        cursor.execute(
            "INSERT INTO payment_methods (payment_method_name) VALUES (%s) RETURNING payment_method_id",
            (payment_method.payment_method_name,)
        )
        conn.commit()
        payment_method_id = cursor.fetchone()[0]
        return {"payment_method_id": payment_method_id, "payment_method_name": payment_method.payment_method_name}
    except errors.UniqueViolation:
        conn.rollback()
        raise HTTPException(status_code=400, detail="Payment method already exists")
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.delete("/payment_methods")
def delete_payment_method(payment_method_id: int):
    cursor.execute(
        "DELETE FROM payment_methods WHERE payment_method_id = %s RETURNING payment_method_id",
        (payment_method_id,)
    )
    result = cursor.fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="Payment method not found")
    conn.commit()
    return {"message": "Payment method deleted successfully"}