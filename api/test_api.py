import requests, os, dotenv, pytest
from faker import Faker
from api.models import User

# Create your tests here.
ENDPOINT = 'http://127.0.0.1:8000/api'
fake = Faker()
token = ''

dotenv.load_dotenv(dotenv.find_dotenv())

def test_run_server():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200

def test_can_obtain_token():    
    payload = {
        'username': os.getenv("admin"),
        'password': os.getenv("admin_password")
    }
    
    response = requests.post(ENDPOINT + '/token', json=payload)
    data = response.json()
    global token
    token = data.get('access')
    
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
    headers = {
        "Authorization": "Bearer " + token
    }

    response = requests.get(ENDPOINT + '/users', headers=headers)
    print(response.json())
    assert response.status_code == 200

def test_can_update_user():
    username = fake.email().split('@')[0]
    headers = {
        "Authorization": "Bearer " + token
    }
    payload = {
        'username': username,        
        'password': 'password',
        'email': 'xchapman@example.net'
    }

    response = requests.patch(ENDPOINT + '/user/2', json=payload, headers=headers)
    assert response.status_code == 200

def test_can_get_user_by_id():
    headers = {
        "Authorization": "Bearer " + token
    }

    response = requests.get(ENDPOINT + '/user/2', headers=headers)
    assert response.status_code == 200

@pytest.mark.django_db(True)
def test_can_delete_user():
    headers = {
        "Authorization": "Bearer " + token
    }
    user = User.objects.last()
    id = user.id
    print(user)

    response = requests.delete(ENDPOINT + f'/user/{id}', headers=headers)
    assert response.status_code == 201

