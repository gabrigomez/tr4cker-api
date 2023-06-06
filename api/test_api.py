import requests

# Create your tests here.
ENDPOINT = 'http://127.0.0.1:8000/api'

def test_run_server():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200

