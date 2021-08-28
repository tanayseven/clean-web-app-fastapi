from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.blog.db_tables import BlogPost
from src.user.functionality import create_auth_token
from test.data.seed_data import create_john_doe_user  # type: ignore


def test_create_blog_is_successful(client: TestClient, db: Session) -> None:
    create_john_doe_user(db)
    auth_token = create_auth_token({"username": "john.doe"})
    headers = {"Authorization": f"Bearer {auth_token}"}
    blog_content = "This is a blog"
    response = client.post(
        "/create-blog", json={"content": blog_content}, headers=headers
    )
    blog_post: BlogPost = db.query(BlogPost).first()
    db.commit()
    assert response.status_code == status.HTTP_201_CREATED
    assert blog_post is not None
    assert blog_post.content == blog_content


def test_create_blog_fails_if_content_is_empty(client: TestClient, db: Session) -> None:
    create_john_doe_user(db)
    auth_token = create_auth_token({"username": "john.doe"})
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.post(
        "/create-blog", json={"content": ""}, headers=headers
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json()['detail'][0]['msg'] == "content cannot be empty"


def test_create_blog_request_fails_when_user_is_not_authenticated(
        client: TestClient,
) -> None:
    dummy_token = "foobar"
    headers = {"Authorization": f"Bearer {dummy_token}"}
    response = client.post(
        "/create-blog", json={"content": "This is a blog"}, headers=headers
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
