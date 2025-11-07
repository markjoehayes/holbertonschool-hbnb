#!/bin/bash

# Test User Registration
echo "Testing User Registration..."
echo "=============================="

response=$(curl -s -w "\n%{http_code}" -X POST http://localhost:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "password": "securepassword123"
  }')

# Extract the body and status code
body=$(echo "$response" | head -n -1)
status_code=$(echo "$response" | tail -n 1)

echo "Status Code: $status_code"
echo "Response: $body"

# Check if successful and extract user_id
if [ "$status_code" -eq 201 ]; then
    user_id=$(echo "$body" | grep -o '"id":"[^"]*' | cut -d'"' -f4)
    echo "User registered successfully!"
    echo "User ID: $user_id"
    
    # Save user_id for retrieval test
    echo "$user_id" > /tmp/user_id.txt
else
    echo "User registration failed"
    exit 1
fi
