from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.core.database import get_db
from app.models.expenses import Expense
from app.schemas.expense import ExpenseCreate, ExpenseUpdate, ExpenseResponse


router = APIRouter()


@router.get("/", response_model=list[ExpenseResponse])
def get_expenses(
    category: str | None = None,
    skip:int= Query(0,ge=0),
    limit:int=Query(10,ge=1,le=100),
    db:Session = Depends(get_db)):
    query = db.query(Expense)

    if category:
        query = query.filter(Expense.category == category)

    expenses = (
        query
        .order_by(desc(Expense.created_at))
        .offset(skip)
        .limit(limit)
        .all()
    )
    return expenses
@router.post("/", response_model=ExpenseResponse, status_code=201)
def create_expense(
    data: ExpenseCreate,
    db: Session = Depends(get_db)
):
    expense = Expense(
        title=data.title,
        amount=data.amount,
        category=data.category
    )

    db.add(expense)
    db.commit()
    db.refresh(expense)

    return expense

@router.get("/{expense_id}", response_model=ExpenseResponse)
def get_expense(
    expense_id: int,
    db: Session = Depends(get_db),
):
    expense = db.query(Expense).filter(Expense.id==expense_id).first()

    if expense is None:
        raise HTTPException(
            status_code= 404,
            detail= "Expense not found"
        )
    return expense

@router.put("/{expense_id}", response_model=ExpenseResponse)
def update_expense(
    expense_id: int,
    data: ExpenseUpdate,
    db:Session = Depends(get_db)
):
    expense = db.query(Expense).filter(Expense.id == expense_id).first()

    if expense is None:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )
    expense.title = data.title
    expense.amount = data.amount
    expense.category = data.category

    db.commit()
    db.refresh(expense)

    return expense

@router.delete("/{expense_id}")
def delete_expense(
    expense_id:int,
    db:Session = Depends(get_db)
):
    expense = db.query(Expense).filter(Expense.id==expense_id).first()

    if expense is None:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )
    db.delete(expense)
    db.commit()

    return {
        "message": "expense deleted"
    }

