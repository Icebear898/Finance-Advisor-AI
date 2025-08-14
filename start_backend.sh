#!/bin/bash

# Start Backend Server
echo "🚀 Starting AI Finance Advisor Backend..."

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -f "backend/app/main.py" ]; then
    echo -e "${YELLOW}Please run this script from the project root directory${NC}"
    exit 1
fi

# Activate virtual environment if it exists
if [ -d "backend/venv" ]; then
    echo -e "${GREEN}Activating virtual environment...${NC}"
    source backend/venv/bin/activate
fi

# Change to backend directory
cd backend

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}Creating .env file from template...${NC}"
    cp env.example .env
    echo -e "${YELLOW}Please edit .env file with your API keys before starting${NC}"
fi

# Start the server
echo -e "${GREEN}Starting FastAPI server on http://localhost:8000${NC}"
echo -e "${GREEN}API Documentation: http://localhost:8000/docs${NC}"
echo -e "${YELLOW}Press Ctrl+C to stop the server${NC}"

# Make sure we're in the backend directory
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
