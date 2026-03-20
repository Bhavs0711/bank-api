from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_banks():
    response = client.get("/banks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_banks_with_limit():
    response = client.get("/banks?limit=5")
    assert response.status_code == 200
    assert len(response.json()) <= 5

def test_get_branches():
    response = client.get("/branches")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_filter_by_city():
    response = client.get("/branches?city=Mumbai")
    assert response.status_code == 200

def test_filter_by_ifsc():
    response = client.get("/branches?ifsc=ABHY0065001")
    assert response.status_code == 200

def test_invalid_route():
    response = client.get("/invalid")
    assert response.status_code == 404