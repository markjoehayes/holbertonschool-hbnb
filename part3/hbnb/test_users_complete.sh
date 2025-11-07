#!/bin/bash

# test_users_complete.sh
echo "Starting Complete User API Test..."
echo "=================================="

# Check if Flask app is running
if ! curl -s http://localhost:5000/api/v1/ > /dev/null; then
    echo "❌ ERROR: Flask app is not running on localhost:5000"
    echo "Please start your Flask app first:"
    echo "  flask run"
    exit 1
fi

echo "✅ Flask app is running"

# Test registration
echo ""
echo "Testing User Registration..."
response=$(curl -s -w "\n%{http_code}" -X POST http://localhost:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe", 
    "email": "john.doe@example.com",
    "password": "securepassword123"
  }')

body=$(echo "$response" | head -n -1)
status_code=$(echo "$response" | tail -n 1)

echo "Status Code: $status_code"
echo "Response: $body"

if [ "$status_code" -eq 201 ]; then
    # Extract user_id from response - FIXED method
    user_id=$(echo "$body" | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])")
    echo "✅ User registered successfully!"
    echo "User ID: $user_id"
else
    echo "❌ User registration failed"
    exit 1
fi

# Test retrieval
echo ""
echo "Testing User Retrieval..."
echo "Retrieving user with ID: $user_id"

response=$(curl -s -w "\n%{http_code}" -X GET "http://localhost:5000/api/v1/users/$user_id")

body=$(echo "$response" | head -n -1)
status_code=$(echo "$response" | tail -n 1)

echo "Status Code: $status_code"
echo "Response: $body"

if [ "$status_code" -eq 200 ]; then
    echo "✅ User retrieved successfully!"
    
    # Verify password is not in response
    if echo "$body" | grep -qi "password"; then
        echo "❌ ERROR: Password found in response!"
        exit 1
    else
        echo "✅ Password correctly excluded from response"
    fi
else
    echo "❌ User retrieval failed"
    exit 1
fi

echo ""
echo "🎉 All tests passed!"
