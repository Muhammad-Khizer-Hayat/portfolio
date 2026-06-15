from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_get_projects():
    res = client.get("/api/projects")
    assert res.status_code == 200
    assert isinstance(res.json(), list)

def test_get_skills():
    res = client.get("/api/skills")
    assert res.status_code == 200
    assert len(res.json()) > 0

def test_contact_missing_fields():
    res = client.post("/api/contact", json={"name": "", "email": "a@b.com", "message": ""})
    assert res.status_code == 400

def test_contact_valid():
    res = client.post("/api/contact", json={
        "name": "Test User",
        "email": "test@example.com",
        "message": "Hello from test!"
    })
    assert res.status_code == 200
    assert res.json()["success"] == True
