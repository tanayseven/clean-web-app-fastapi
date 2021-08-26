from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.user.functionality import create_auth_token
from test.data.seed_data import create_john_doe_user  # type: ignore


def test_create_blog_is_successful(client: TestClient, db: Session) -> None:
    create_john_doe_user(db)
    auth_token = create_auth_token({"username": "john.doe"})
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.post(
        "/create-blog", json={"content": "This is a blog"}, headers=headers
    )
    assert response.status_code == status.HTTP_201_CREATED


def test_create_blog_request_fails_when_user_is_not_authenticated(
    client: TestClient,
) -> None:
    token = "foobar"
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post(
        "/create-blog", json={"content": "This is a blog"}, headers=headers
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
