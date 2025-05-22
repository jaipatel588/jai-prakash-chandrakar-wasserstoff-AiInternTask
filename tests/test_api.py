from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_query():
    res = client.get("/query/", params={"q": "What is this document about?"})
    assert res.status_code == 200