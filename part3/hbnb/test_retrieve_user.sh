#!/bin/bash

# Test User Retrieval
echo "Testing User Retrieval..."
echo "=========================="

# Get the user_id from previous test
if [ -f /tmp/user_id.txt ]; then
    user_id=$(cat /tmp/user_id.txt)
else
    echo "No user ID found. Run registration test first."
    exit 1
fi

response=$(curl -s -w "\n%{http_code}" -X GET "http://localhost:5000/api/v1/users/$user_id")

# Extract the body and status code
body=$(echo "$response" | head -n -1)
status_code=$(echo "$response" | tail -n 1)

echo "Status Code: $status_code"
echo "Response: $body"

if [ "$status_code" -eq 200 ]; then
    echo "✅ User retrieved successfully!"
    
    # Verify password is not in response
    if echo "$body" | grep -q "password"; then
        echo "ERROR: Password found in response!"
        exit 1
    else
        echo "✅ Password correctly excluded from response"
    fi
else
    echo "User retrieval failed"
    exit 1
fi
