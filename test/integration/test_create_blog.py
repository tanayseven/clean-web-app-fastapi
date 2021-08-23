import pytest
from fastapi.testclient import TestClient
from fastapi import status


@pytest.mark.skip()
def test_create_blog_is_successful(client: TestClient) -> None:
    response = client.post("/create-blog/", json={"content": "This is a blog"})
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.skip()
def test_create_blog_request_fails_when_user_is_not_authenticated(client: TestClient) -> None:
    token = "foobar"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = client.post("/create-blog/", json={"content": "This is a blog"}, headers=headers)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
