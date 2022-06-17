from venv import create
from fastapi.testclient import TestClient
from sqlalchemy import  create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import  declarative_base
from app.main import app  
from app import schemas
from app.config import settings
from app.database import get_db
from app.database import Base
import pytest
from alembic import command
from app.oauth2 import create_access_token
from app import models


#SQLALCHEMY_DATABASE_URL =  'postgresql://postgres:S.18112006.k@localhost:5432/test'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine= create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



@pytest.fixture(scope='function')
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope='function')
def client(session):
    def overrid_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = overrid_get_db
    yield TestClient(app)
    

@pytest.fixture
def test_user2(client):
    user_data = {'email': 'sameer123@gmail.com', 'password': '18112006'}
    res = client.post('/users/', json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user



@pytest.fixture
def test_user(client):
    user_data = {'email': 'sameer@gmail.com', 'password': '18112006'}
    res = client.post('/users/', json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token(data={'user_id': test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {**client.headers, 'Authorization': f'Bearer {token}'}

    return client

@pytest.fixture
def test_posts(test_user, session, test_user2):
    posts_data = [
        {
            'title': '1st_title',
            'content': '1st_content',
            'owner_id': test_user['id']
        },
        {
            'title': '2nd_title',
            'content': '2nd_content',
            'owner_id': test_user['id']
        },
        {
            'title': '3rd_title',
            'content': '3rd_content',
            'owner_id': test_user['id'] 
        },
        {
            'title': '3rd_title',
            'content': '3rd_content',
            'owner_id': test_user2['id'] 
        }
    ]

    def create_post_model(post):
        return models.Post(**post)


    post_map = map(create_post_model, posts_data)

    posts = list(post_map)
    
    session.add_all(posts)
    session.commit()

    posts = session.query(models.Post).all()

    return posts