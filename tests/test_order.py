import json


def test_index(client):
    response = client.get('/order/')
    assert response.status_code == 200
    res_data = json.loads(response.data)
    assert len(res_data) > 0
