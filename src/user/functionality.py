from datetime import timedelta, datetime
from typing import Optional, Tuple

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError  # type: ignore
from passlib.context import CryptContext  # type: ignore
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette import status

from src.config import config
from src.database import get_db
from src.user.db_tables import User

pwd_context = CryptContext(
    schemes=[config.get("security", "encryption-scheme")], deprecated="auto"
)
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_user(db: Session, username: str, password: str, email: str) -> None:
    try:
        user = User(
            username=username,
            password=password,
            email=email,
        )
        db.add(user)
        db.commit()
    except IntegrityError:
        raise UserExistsError


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    authentication_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid auth credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: Optional[str] = payload.get("username")
    except JWTError:
        raise authentication_exception
    if username is None:
        raise authentication_exception
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise authentication_exception
    return user


def hash_password(password: str) -> str:
    return pwd_context.hash(password)  # type: ignore


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)  # type: ignore


def create_auth_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta is not None:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    auth_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return auth_token  # type: ignore


async def authenticate_user(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
) -> Tuple[bool, str]:
    user: Optional[User] = (
        db.query(User).filter(User.username == form_data.username).first()
    )
    user_exists = user is not None
    password_is_valid = False
    if user is not None:
        password_is_valid = verify_password(form_data.password, user.password)
    user_is_authenticated = user_exists and password_is_valid
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    auth_token = create_auth_token(
        {"username": f"{form_data.username}"}, expires_delta=access_token_expires
    )
    return user_is_authenticated, auth_token


def login_user(db: Session, username: str, password: str) -> bool:
    user = db.query(User).filter(User.username == username).first()
    return user is not None and user.password == password


class UserExistsError(Exception):
    pass
