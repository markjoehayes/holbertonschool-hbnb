curl -X POST "http://127.0.0.1:5000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "DebugUser",
    "last_name": "Test",
    "email": "debuguser@example.com",
    "password": "debugpass123"
  }'

curl -X POST "http://127.0.0.1:5000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "debuguser@example.com",
    "password": "debugpass123"
  }'
