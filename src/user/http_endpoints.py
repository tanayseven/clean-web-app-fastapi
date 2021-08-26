from typing import Union

from fastapi import APIRouter, Depends, status
from fastapi.responses import Response
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError  # type: ignore
from passlib.context import CryptContext  # type: ignore
from pydantic.main import BaseModel
from sqlalchemy.orm import Session

from src.database import get_db
from src.responses import DetailResponse
from src.user.functionality import create_user, authenticate_user, UserExistsError

router = APIRouter()


class SignUpRequest(BaseModel):
    username: str
    password: str
    email: str


@router.post("/user/sign-up", tags=["user", "sign-up"], response_model=DetailResponse)
async def user_sign_up(
    sign_up_request: SignUpRequest, response: Response, db: Session = Depends(get_db)
) -> DetailResponse:
    try:
        create_user(
            db,
            username=sign_up_request.username,
            password=sign_up_request.password,
            email=sign_up_request.email,
        )
    except UserExistsError:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return DetailResponse(detail="failed to create user, user already exists")
    else:
        response.status_code = status.HTTP_201_CREATED
        return DetailResponse(detail="sign up successful")


class DetailResponseWithToken(BaseModel):
    detail: str
    token: str


@router.post(
    "/user/login",
    tags=["user", "login"],
    response_model=Union[DetailResponseWithToken, DetailResponse],  # type: ignore
)
async def user_login(
    response: Response,
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Union[DetailResponseWithToken, DetailResponse]:
    user_is_authenticated, auth_token = await authenticate_user(form_data, db)
    if user_is_authenticated:
        return DetailResponseWithToken(
            detail="login successful",
            token=f"{auth_token}",
        )
    response.status_code = status.HTTP_401_UNAUTHORIZED
    return DetailResponse(detail="Invalid auth credentials")
