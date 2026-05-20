from fastapi.testclient import TestClient
from ..main import app
from fastapi import status

# Bind the main app into the TestClient
client = TestClient(app)

def test_health():
    response = client.get("/healthy")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "Healthy"}