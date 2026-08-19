from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.core.database import get_db
from app.core.security import hash_password
from app.models.users import User
from app.schemas.user import UserCreate, UserResponse
from app.core.security import create_access_token, hash_password,verify_password

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

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = (
        db.query(User)
        .filter(User.username == form_data.username)
        .first()
    )
    if not user or not verify_password(
        form_data.password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=401,
            detail="Incorrect Username or Password"
        )
    access_token = create_access_token(user.id)

    return{
        "access_token": access_token,
        "token_type": "bearer"
    }
