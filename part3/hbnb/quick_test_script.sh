#!/bin/bash
# Use the real token from your login response
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

# Test other protected endpoints:
curl -X PUT "http://127.0.0.1:5000/api/v1/places/9dfd31f9-de13-48d4-9868-b541af7a04e6" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Place Name"}'

# Test reviews endpoint
curl -X POST "http://127.0.0.1:5000/api/v1/reviews/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Great place!",
    "rating": 5,
    "place_id": "9dfd31f9-de13-48d4-9868-b541af7a04e6"
  }'
