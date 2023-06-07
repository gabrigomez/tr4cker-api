import requests
from faker import Faker

# Create your tests here.
ENDPOINT = 'http://127.0.0.1:8000/api'

def test_run_server():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200

def test_can_post_user():
    fake = Faker()

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
    



    

