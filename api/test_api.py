import requests
from faker import Faker

# Create your tests here.
ENDPOINT = 'http://127.0.0.1:8000/api'
fake = Faker()

def test_run_server():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200

def test_can_post_user():
    email:str = fake.email()
    username = email.split('@')
    password = fake.password(length=6, special_chars=False)

    payload = {
        'username': username[0],
        'email': email,
        'password': password
    }

    print(payload)
    response = requests.post(ENDPOINT + '/register', json=payload)
    assert response.status_code == 201

def test_can_get_all_users():
    response = requests.get(ENDPOINT + '/users')
    assert response.status_code == 200

def test_can_update_user():
    username = fake.email().split('@')[0]    

    payload = {
        'username': username,        
        'password': 'password',
        'email': 'xchapman@example.net'
    }

    response = requests.patch(ENDPOINT + '/user/2', json=payload)
    assert response.status_code == 200