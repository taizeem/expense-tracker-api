from datetime import datetime, timedelta, timezone
from pwdlib import PasswordHash
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt

from app.core.config import settings

oaut2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")
password_hash = PasswordHash.recommended()

def hash_password(password: str) -> str:
    return password_hash.hash(password)

def verify_password(password: str, hashed_password) -> bool:
    return password_hash.verify(password, hashed_password)

def create_access_token(user_id: int) ->str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)

    payload = {
        "sub": str(user_id),
        "exp": expire,
    }
    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm="HS256",
    )
def get_current_user(
        token: str = Depends(oaut2_scheme)
):
    try: 
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=["HS256"]
        )
        user_id = int(payload["sub"])
    except(jwt.InvalidTokenError,KeyError,ValueError):
        raise HTTPException(
            status_code=401,
            detail="invalid or expired token"
        )
    return user_id