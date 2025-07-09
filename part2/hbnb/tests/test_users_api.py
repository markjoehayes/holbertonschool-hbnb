# tests/test_users_api.py
import pytest
from app import create_app
from app.services.facade import facade
from models.user import User

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_create_and_get_user(client):
    # Test user creation
    response = client.post('/api/v1/users/', json={
        'first_name': 'Test',
        'last_name': 'User',
        'email': 'test@example.com'
    })
    assert response.status_code == 201
    user_id = response.json['id']
    
    # Test getting the user
    response = client.get(f'/api/v1/users/{user_id}')
    assert response.status_code == 200
    assert response.json['email'] == 'test@example.com'

def test_get_all_users(client):
    # Create a test user
    facade.create_user({
        'first_name': 'Test1',
        'last_name': 'User1',
        'email': 'test1@example.com'
    })
    
    # Get all users
    response = client.get('/api/v1/users/')
    assert response.status_code == 200
    assert len(response.json) >= 1

def test_update_user(client):
    # Create a test user
    user = facade.create_user({
        'first_name': 'Original',
        'last_name': 'User',
        'email': 'original@example.com'
    })
    
    # Update the user
    response = client.put(f'/api/v1/users/{user.id}', json={
        'first_name': 'Updated',
        'last_name': 'User',
        'email': 'updated@example.com'
    })
    assert response.status_code == 200
    assert response.json['first_name'] == 'Updated'
    assert response.json['email'] == 'updated@example.com'

def test_duplicate_email(client):
    # Create first user
    response = client.post('/api/v1/users/', json={
        'first_name': 'First',
        'last_name': 'User',
        'email': 'duplicate@example.com'
    })
    assert response.status_code == 201
    
    # Try to create second user with same email
    response = client.post('/api/v1/users/', json={
        'first_name': 'Second',
        'last_name': 'User',
        'email': 'duplicate@example.com'
    })
    assert response.status_code == 400
    assert 'already registered' in response.json['error']
