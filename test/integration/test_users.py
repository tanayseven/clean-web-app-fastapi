from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from fastapi import status

from src.users.db_tables import User
from src.users.http_endpoints import hash_password


def test_login_success(client: TestClient, db: Session) -> None:
    _create_john_doe_user(db)
    response = client.post(
        f"/user/login", data={"username": "john.doe", "password": "password"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "login successful", "token": "john.doe"}


def test_login_with_invalid_username_fails(client: TestClient, db: Session) -> None:
    _create_john_doe_user(db)
    response = client.post(
        f"/user/login", data={"username": "foo.bar", "password": "password"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"message": "Invalid auth credentials"}


def test_login_with_invalid_password_fails(client: TestClient, db: Session) -> None:
    _create_john_doe_user(db)
    response = client.post(
        f"/user/login", data={"username": "john.doe", "password": "foobar"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"message": "Invalid auth credentials"}


def test_sign_up_successful(client: TestClient) -> None:
    user_sign_up = {
        "username": "john.doe",
        "password": "password",
        "email": "john.doe@company.com",
    }
    response = client.post(f"/user/sign-up", json=user_sign_up)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {"message": "sign up successful"}


def test_sign_up_fails_when_user_exists(client: TestClient, db: Session) -> None:
    _create_john_doe_user(db)
    user_sign_up = {
        "username": "john.doe",
        "password": "password",
        "email": "john.doe@company.com",
    }
    response = client.post(f"/user/sign-up", json=user_sign_up)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"message": "failed to create user, user already exists"}


def _create_john_doe_user(db: Session) -> None:
    user = User(username="john.doe", password=hash_password("password"), email="john.doe@company.com")
    db.add(user)
    db.commit()
