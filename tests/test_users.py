from tkinter import N
import pytest
from app import schemas
from jose import jwt
from app.config import settings



# def test_root(client):
#     res = client.get('/')
#     print(res.json().get('message'))
#     assert res.json().get('message') == 'Hello World!'
#     assert res.status_code == 200

def test_create_user(client):
    res = client.post('/users/', json={'email': 'hello1@gmail.com', 'password': '18112006'})
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == 'hello1@gmail.com'
    assert res.status_code == 201

def test_login_user(test_user, client):
    res = client.post('/login', data={'username': test_user['email'], 'password': test_user['password']})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, settings.algorithm)
    id : str = payload.get('user_id')
    assert id == test_user['id']
    assert login_res.token_type == 'bearer'
    assert res.status_code == 200

@pytest.mark.parametrize('email, password, status_code', [
    ('wrongemail@gmail.com', '18112006', 403), 
    ('sameer@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassoword', 403),
    (None, '18112006', 422),
    ('sameer@gmail.com', None, 422)
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post('/login', data={'username': email, 'password': password})

    assert res.status_code == status_code
    #assert res.json().get('detail') == 'Invalid Credentials!'