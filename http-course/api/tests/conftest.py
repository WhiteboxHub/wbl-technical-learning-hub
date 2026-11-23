import os
import tempfile

# Tests never touch the Postgres database: point the app at a throwaway SQLite file
# before the app module is imported.
_db = os.path.join(tempfile.mkdtemp(), "test.db")
os.environ["DATABASE_URL"] = f"sqlite:///{_db}"
os.environ["DEMO_PASSWORD"] = "pytest-only-password"

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:  # runs startup: creates tables and seeds 20 employees
        yield c


def new_employee(**overrides):
    body = {
        "name": "Test Person", "email": "test.person@example.com", "title": "Tester",
        "department_id": 2, "manager_id": 2, "hire_date": "2024-01-15", "salary": 90000,
    }
    body.update(overrides)
    return body
