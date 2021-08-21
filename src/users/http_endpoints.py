from fastapi import APIRouter, Depends, status
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


@router.post("/user/login", tags=["users", "login"])
async def user_login(
    login_request: LoginRequest, response: Response, db: Session = Depends(get_db)
) -> dict:
    login_successful = login_user(
        db, username=login_request.username, password=login_request.password
    )
    if login_successful:
        return {"message": "login successful"}
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "login failed"}
