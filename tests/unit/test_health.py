"""Unit tests for the planner app (no browser, no real DB)."""
import pytest

from app import app


@pytest.fixture
def client():
    """Flask test client."""
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def test_health_returns_200_and_healthy(client):
    """GET /health returns 200 with status healthy."""
    rv = client.get("/health")
    assert rv.status_code == 200
    data = rv.get_json()
    assert data == {"status": "healthy"}
