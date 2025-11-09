import requests
import time

BASE_URL = "http://127.0.0.1:5000/api/v1"

# Create unique email with timestamp
unique_email = f"test{int(time.time())}@example.com"

print(f"Testing with email: {unique_email}")

# 1. Register user
register_data = {
    "first_name": "Test",
    "last_name": "User",
    "email": unique_email,
    "password": "test123"
}

print("1. Registering user...")
register_response = requests.post(f"{BASE_URL}/users/", json=register_data)
print(f"   Status: {register_response.status_code}")
print(f"   Response: {register_response.text}")

if register_response.status_code == 201:
    # 2. Login with same credentials
    login_data = {
        "email": unique_email,
        "password": "test123"
    }
    
    print("2. Logging in...")
    login_response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print(f"   Status: {login_response.status_code}")
    print(f"   Response: {login_response.text}")
    
    if login_response.status_code == 200:
        print("🎉 SUCCESS! Authentication is working!")
        token = login_response.json().get('access_token')
        print(f"   Token: {token[:50]}...")
    else:
        print("❌ Login failed")
else:
    print("❌ Registration failed")
