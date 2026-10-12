import pytest
from app import create_app
from database.db import db


@pytest.fixture(autouse=True)
def reset_database():
    db.reset()
    yield


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as test_client:
        yield test_client
