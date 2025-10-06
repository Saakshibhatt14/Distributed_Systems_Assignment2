#!/bin/bash

# Performance Testing Script for Banking System
# Tests both Layered and Microservice architectures

echo "=========================================="
echo "Banking System Performance Testing"
echo "=========================================="
echo

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python3 is not installed"
    exit 1
fi

# Install requirements
echo "Installing requirements..."
pip3 install -r requirements.txt
echo

# Function to test architecture
test_architecture() {
    local architecture=$1
    local url=$2
    local output_file=$3
    
    echo "Testing $architecture architecture..."
    echo "API URL: $url"
    echo
    
    # Check if API is running
    if ! curl -s "$url/health" > /dev/null; then
        echo "Error: $architecture API is not running at $url"
        echo "Please start the system with: docker-compose up"
        return 1
    fi
    
    # Run performance test
    python3 load_test.py --architecture $architecture --url $url --output $output_file
    
    if [ $? -eq 0 ]; then
        echo "✅ $architecture test completed successfully"
    else
        echo "❌ $architecture test failed"
        return 1
    fi
    echo
}

# Test Layered Architecture
echo "1. Testing Layered Architecture"
echo "================================"
test_architecture "layered" "http://localhost:3001" "layered_performance_results.json"

# Test Microservice Architecture  
echo "2. Testing Microservice Architecture"
echo "====================================="
test_architecture "microservice" "http://localhost:3000" "microservice_performance_results.json"

# Compare results
echo "3. Comparing Results"
echo "===================="
if [ -f "layered_performance_results.json" ] && [ -f "microservice_performance_results.json" ]; then
    python3 compare_results.py --layered layered_performance_results.json --microservice microservice_performance_results.json
    echo "✅ Comparison completed successfully"
else
    echo "❌ Cannot compare results - one or both test files are missing"
    exit 1
fi

echo
echo "=========================================="
echo "Performance testing completed!"
echo "=========================================="

