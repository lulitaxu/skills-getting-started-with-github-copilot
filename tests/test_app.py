"""Backend tests for the Mergington High School API (AAA pattern). Written by Muse."""
from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)


def test_get_activities_returns_all_activities():
    # Arrange / Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    assert "Chess Club" in response.json()
    assert len(response.json()) >= 9


def test_signup_for_activity_succeeds():
    # Arrange
    email = "newstudent@mergington.edu"
    if email in activities["Chess Club"]["participants"]:
        activities["Chess Club"]["participants"].remove(email)
    # Act
    response = client.post("/activities/Chess Club/signup", params={"email": email})
    # Assert
    assert response.status_code == 200
    assert email in activities["Chess Club"]["participants"]


def test_signup_duplicate_is_rejected():
    # Arrange
    email = activities["Chess Club"]["participants"][0]
    # Act
    response = client.post("/activities/Chess Club/signup", params={"email": email})
    # Assert
    assert response.status_code == 400


def test_signup_unknown_activity_returns_404():
    # Arrange / Act
    response = client.post("/activities/No Such Club/signup", params={"email": "a@mergington.edu"})
    # Assert
    assert response.status_code == 404


def test_unregister_removes_participant():
    # Arrange
    email = "temp@mergington.edu"
    activities["Science Club"]["participants"].append(email)
    # Act
    response = client.request("DELETE", "/activities/Science Club/unregister", params={"email": email})
    # Assert
    assert response.status_code == 200
    assert email not in activities["Science Club"]["participants"]
