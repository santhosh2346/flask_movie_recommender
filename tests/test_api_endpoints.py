import os
import json
import pytest
from run import app
from app.preprocessing import build_and_save, PROCESSED

@pytest.fixture(scope="module")
def client():
    if not os.path.exists(PROCESSED) or not os.listdir(PROCESSED):
        build_and_save()
    app.testing = True
    with app.test_client() as c:
        yield c

def test_recommend_endpoint(client):
    res = client.get("/recommend?title=The%20Matrix&n=3")
    assert res.status_code in (200, 404)
    data = res.get_json()
    assert isinstance(data, dict)

def test_recommend_text_endpoint(client):
    payload = {"plot": "A hacker discovers a simulated reality", "n": 3}
    res = client.post("/recommend_text", data=json.dumps(payload), content_type='application/json')
    assert res.status_code == 200
    data = res.get_json()
    assert 'recommendations' in data
