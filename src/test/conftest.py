from src.db.main import get_session
from src.auth.dependencies import AcessTokenBearer, RoleChecker, RefreshTokenBearer
from src import app
from unittest.mock import Mock
import pytest
from fastapi.testclient import TestClient

mock_session = Mock()
mock_auth_service = Mock()
mock_book_service = Mock()


def get_mock_session():
    yield mock_session


role_checker = RoleChecker("user")
auth_user = AcessTokenBearer()

app.dependency_overrides[get_session] = get_mock_session
app.dependency_overrides[role_checker] = Mock()
app.dependency_overrides[auth_user] = Mock()


@pytest.fixture
def fake_session():
    return mock_session


@pytest.fixture
def fake_auth_service():
    return mock_auth_service


@pytest.fixture
def fake_book_service():
    return mock_book_service


@pytest.fixture
def test_client():
    return TestClient(app=app)
