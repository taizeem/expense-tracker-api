from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import hash_password
from app.models.users import User
from app.schemas.user import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/",response_model=UserResponse, status_code=201)
def create_user(data: UserCreate, db:Session = Depends(get_db)):
    existing_user = (
        db.query(User)
        .filter(User.username == data.username)
        .first()
    )
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )
    user = User(
        username=data.username,
        password_hash=hash_password(data.password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user
    