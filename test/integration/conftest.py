from typing import Generator

import pytest
import requests
from fastapi.testclient import TestClient
from requests.adapters import HTTPAdapter
from sqlalchemy.orm import Session
from urllib3 import Retry  # type: ignore

from src.database import get_db, engine
from src.db_tables import tables
from src.main import app


@pytest.fixture(scope="function", autouse=True)
def wait_for_api(function_scoped_container_getter) -> (requests.Session, str):
    """Wait for the api from my_api_service to become responsive"""
    request_session = requests.Session()
    retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
    request_session.mount("http://", HTTPAdapter(max_retries=retries))

    service = function_scoped_container_getter.get("adminer").network_info[0]
    api_url = "http://%s:%s/" % (service.hostname, service.host_port)
    assert request_session.get(api_url)
    return request_session, api_url


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    yield TestClient(app=app)


@pytest.fixture
def db() -> Generator[Session, None, None]:
    yield next(get_db())


@pytest.fixture(scope="function", autouse=True)
def reset_tables() -> Generator[None, None, None]:
    [table.__table__.create(engine) for table in tables]
    yield
    [table.__table__.drop(engine) for table in tables]
