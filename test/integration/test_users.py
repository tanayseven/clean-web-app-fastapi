import re

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from fastapi import status

from test.data.seed_data import create_john_doe_user  # type: ignore


def is_valid_format_for_auth_token(auth_token: str) -> bool:
    regex = re.compile(r"[A-Za-z0-9-_]*\.[A-Za-z0-9-_]*\.[A-Za-z0-9-_]*$")
    return regex.fullmatch(auth_token) is not None


def test_login_success(client: TestClient, db: Session) -> None:
    create_john_doe_user(db)
    response = client.post(
        f"/user/login", data={"username": "john.doe", "password": "password"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["detail"] == "login successful"
    assert is_valid_format_for_auth_token(response.json()["token"])


def test_login_with_invalid_username_fails(client: TestClient, db: Session) -> None:
    create_john_doe_user(db)
    response = client.post(
        f"/user/login", data={"username": "foo.bar", "password": "password"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Invalid auth credentials"}


def test_login_with_invalid_password_fails(client: TestClient, db: Session) -> None:
    create_john_doe_user(db)
    response = client.post(
        f"/user/login", data={"username": "john.doe", "password": "foobar"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Invalid auth credentials"}


def test_sign_up_successful(client: TestClient) -> None:
    user_sign_up = {
        "username": "john.doe",
        "password": "password",
        "email": "john.doe@company.com",
    }
    response = client.post(f"/user/sign-up", json=user_sign_up)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {"detail": "sign up successful"}


def test_sign_up_fails_when_user_exists(client: TestClient, db: Session) -> None:
    create_john_doe_user(db)
    user_sign_up = {
        "username": "john.doe",
        "password": "password",
        "email": "john.doe@company.com",
    }
    response = client.post(f"/user/sign-up", json=user_sign_up)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "failed to create user, user already exists"}


def test_sign_up_fails_when_invalid_email_address_is_given(client: TestClient, db: Session) -> None:
    create_john_doe_user(db)
    user_sign_up = {
        "username": "john.doe",
        "password": "password",
        "email": "foo.bar",
    }
    response = client.post(f"/user/sign-up", json=user_sign_up)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json()["detail"][0]["msg"] == "invalid email address"
