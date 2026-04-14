import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"]["participants"], list)

def test_signup():
    response = client.post("/activities/Chess Club/signup", params={"email": "test@example.com"})
    assert response.status_code == 200
    assert "Signed up test@example.com for Chess Club" == response.json()["message"]

def test_signup_already_signed():
    # First signup
    client.post("/activities/Programming Class/signup", params={"email": "already@example.com"})
    # Second
    response = client.post("/activities/Programming Class/signup", params={"email": "already@example.com"})
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

def test_signup_activity_not_found():
    response = client.post("/activities/Nonexistent/signup", params={"email": "test@example.com"})
    assert response.status_code == 404

def test_unregister():
    # First signup
    client.post("/activities/Gym Class/signup", params={"email": "unreg@example.com"})
    # Then unregister
    response = client.delete("/activities/Gym Class/participants/unreg@example.com")
    assert response.status_code == 200
    assert "Unregistered unreg@example.com from Gym Class" == response.json()["message"]

def test_unregister_not_signed():
    response = client.delete("/activities/Chess Club/participants/notsigned@example.com")
    assert response.status_code == 404

def test_unregister_activity_not_found():
    response = client.delete("/activities/Nonexistent/participants/test@example.com")
    assert response.status_code == 404