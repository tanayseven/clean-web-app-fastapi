from typing import Optional

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic.main import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from fastapi.responses import Response

from src.database import get_db
from src.users.db_tables import User

router = APIRouter()


class SignUpRequest(BaseModel):
    username: str
    password: str
    email: str


class UserExistsError(Exception):
    pass


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")


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


@router.post("/user/sign-up", tags=["users", "sign-up"])
async def user_sign_up(
        sign_up_request: SignUpRequest, response: Response, db: Session = Depends(get_db)
) -> dict:
    try:
        create_user(
            db,
            username=sign_up_request.username,
            password=sign_up_request.password,
            email=sign_up_request.email,
        )
    except UserExistsError:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "failed to create user, user already exists"}
    else:
        response.status_code = status.HTTP_201_CREATED
        return {"message": "sign up successful"}


class LoginRequest(BaseModel):
    username: str
    password: str


def login_user(db: Session, username: str, password: str) -> bool:
    user = db.query(User).filter(User.username == username).first()
    return user is not None and user.password == password


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    user = db.query(User).filter(User.username == token).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid auth credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return user


def hash_password(password: str) -> str:
    return f"hash+{password}"


@router.post("/user/login", tags=["users", "login"])
async def user_login(
        response: Response, db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> dict:
    login_successful: Optional[User] = db.query(User).filter(User.username == form_data.username).first()
    if login_successful is None or login_successful.password != hash_password(form_data.password):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"message": "Invalid auth credentials"}
    return {"message": "login successful", "token": f"{form_data.username}"}


class CreateBlogRequest(BaseModel):
    content: str


@router.post("/create-blog", tags=["blogs"])
async def create_blog(create_blog_request: CreateBlogRequest, current_user: User = Depends(get_current_user)) -> dict:
    return {"message": f"Successfully authenticated {current_user.username}"}
