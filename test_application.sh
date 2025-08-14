#!/bin/bash

# Test AI Finance Advisor Application
echo "🧪 Testing AI Finance Advisor Application..."

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to test backend
test_backend() {
    echo -e "${YELLOW}Testing Backend API...${NC}"
    
    # Test health endpoint
    echo "Testing health endpoint..."
    if curl -s http://localhost:8000/health > /dev/null; then
        echo -e "${GREEN}✅ Backend health check passed${NC}"
    else
        echo -e "${RED}❌ Backend health check failed${NC}"
        return 1
    fi
    
    # Test chat endpoint
    echo "Testing chat endpoint..."
    response=$(curl -s -X POST http://localhost:8000/api/chat \
        -H "Content-Type: application/json" \
        -d '{"message": "Hello, how are you?"}')
    
    if echo "$response" | grep -q "message"; then
        echo -e "${GREEN}✅ Chat endpoint working${NC}"
    else
        echo -e "${RED}❌ Chat endpoint failed${NC}"
        return 1
    fi
    
    # Test market data endpoint
    echo "Testing market data endpoint..."
    if curl -s http://localhost:8000/api/finance/market-summary > /dev/null; then
        echo -e "${GREEN}✅ Market data endpoint working${NC}"
    else
        echo -e "${RED}❌ Market data endpoint failed${NC}"
        return 1
    fi
    
    return 0
}

# Function to test frontend
test_frontend() {
    echo -e "${YELLOW}Testing Frontend...${NC}"
    
    # Check if frontend is accessible
    if curl -s http://localhost:3000 > /dev/null; then
        echo -e "${GREEN}✅ Frontend is accessible${NC}"
    else
        echo -e "${RED}❌ Frontend is not accessible${NC}"
        return 1
    fi
    
    return 0
}

# Main test function
main() {
    echo "Starting application tests..."
    echo "Make sure both backend and frontend are running!"
    echo ""
    
    # Test backend
    if test_backend; then
        echo -e "${GREEN}🎉 Backend tests passed!${NC}"
    else
        echo -e "${RED}💥 Backend tests failed!${NC}"
        echo "Make sure the backend is running on http://localhost:8000"
        return 1
    fi
    
    echo ""
    
    # Test frontend
    if test_frontend; then
        echo -e "${GREEN}🎉 Frontend tests passed!${NC}"
    else
        echo -e "${RED}💥 Frontend tests failed!${NC}"
        echo "Make sure the frontend is running on http://localhost:3000"
        return 1
    fi
    
    echo ""
    echo -e "${GREEN}🎉 All tests passed! Your AI Finance Advisor is working correctly!${NC}"
    echo ""
    echo "You can now:"
    echo "  • Open http://localhost:3000 to use the application"
    echo "  • View API docs at http://localhost:8000/docs"
    echo "  • Test the chat functionality"
    echo "  • Upload documents for analysis"
    echo "  • Use the financial calculators"
}

# Run tests
main
