#!/bin/bash

echo "Starting Complete User API Test..."
echo "=================================="

# Run registration test
./test_register_user.sh
if [ $? -ne 0 ]; then
    echo "Registration test failed"
    exit 1
fi

echo ""
echo "Waiting 1 second before retrieval test..."
sleep 1

# Run retrieval test
./test_retrieve_user.sh
if [ $? -ne 0 ]; then
    echo " Retrieval test failed"
    exit 1
fi

echo ""
echo "All tests passed!"
