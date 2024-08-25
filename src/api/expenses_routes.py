from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from src.database.db_connection import conn, cursor
from dotenv import load_dotenv
from datetime import date
from decimal import Decimal
from typing import Optional

load_dotenv()

router = APIRouter()    

class ExpenseCreate(BaseModel):
    date: date
    category_id: int
    description: str
    amount: Decimal
    vat: Decimal
    payment_method_id: int
    business_personal: str

@router.get("/expenses")
def get_expenses(
    category_id: Optional[int] = None,
    payment_method_id: Optional[int] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
):
    sql_query = "SELECT * FROM expenses"
    query_params = []
    where_clauses = []

    if category_id is not None:
        where_clauses.append("category_id = %s")
        query_params.append(category_id)

    if payment_method_id is not None:
        where_clauses.append("payment_method_id = %s")
        query_params.append(payment_method_id)

    if start_date is not None:
        where_clauses.append("date >= %s")
        query_params.append(start_date)

    if end_date is not None:
        where_clauses.append("date <= %s")
        query_params.append(end_date)

    if where_clauses:
        sql_query += " WHERE " + " AND ".join(where_clauses)

    cursor.execute(sql_query, tuple(query_params))
    expenses = cursor.fetchall()

    if not expenses:
        raise HTTPException(status_code=404, detail="No expenses found for the given filters")
    
    return [
        {
            "transaction_id": e[0],
            "date": e[1],
            "category_id": e[2],
            "description": e[3],
            "amount": e[4],
            "vat": e[8],
            "payment_method_id": e[5],
            "business_personal": e[6],
        } 
        for e in expenses
    ]


@router.post("/expenses", status_code=201)
def create_expense(expense: ExpenseCreate):
    cursor.execute(
        "INSERT INTO expenses (date, category_id, description, amount, vat, payment_method_id, business_personal)"
        "VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING transaction_id",
        (
            expense.date,
            expense.category_id,
            expense.description,
            expense.amount,
            expense.vat,
            expense.payment_method_id,
            expense.business_personal,
        ),
    )
    conn.commit()
    transaction_id = cursor.fetchone()[0]
    return {"transaction_id": transaction_id, "description": expense.description}

@router.delete("/expenses")
def delete_expense(transaction_id: int = Query(
    ...,
    description="The ID of the transaction to delete",
)):
    cursor.execute(
    "DELETE FROM expenses WHERE transaction_id = %s RETURNING transaction_id",
    (transaction_id),
    )
    result = cursor.fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="Expense not found")
    conn.commit()
    return {"message": "Expense deleted successfully"}


