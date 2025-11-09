# Register a user
curl -X POST "http://127.0.0.1:5000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "SimpleTest",
    "last_name": "User",
    "email": "simpletest123@example.com", 
    "password": "simplepass"
  }'

# Login with same user
curl -X POST "http://127.0.0.1:5000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "simpletest123@example.com",
    "password": "simplepass"
  }'
