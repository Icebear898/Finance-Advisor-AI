#!/bin/bash

echo "🚀 Starting AI Finance Advisor with Authentication System"
echo "=================================================="

# Check if backend is running
if ! curl -s http://localhost:8000/health > /dev/null; then
    echo "📡 Starting Backend Server..."
    cd backend
    
    # Check if .env exists
    if [ ! -f .env ]; then
        echo "⚠️  .env file not found. Creating from example..."
        cp env.example .env
        echo "📝 Please edit backend/.env with your API keys:"
        echo "   - GOOGLE_GEMINI_API_KEY"
        echo "   - SECRET_KEY (generate a secure random key)"
        echo "   - Other API keys as needed"
        echo ""
        echo "💡 You can generate a secret key with:"
        echo "   python -c \"import secrets; print(secrets.token_urlsafe(32))\""
        echo ""
        read -p "Press Enter after updating .env file..."
    fi
    
    # Start backend
    python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
    BACKEND_PID=$!
    echo "✅ Backend started with PID: $BACKEND_PID"
    
    # Wait for backend to be ready
    echo "⏳ Waiting for backend to be ready..."
    for i in {1..30}; do
        if curl -s http://localhost:8000/health > /dev/null; then
            echo "✅ Backend is ready!"
            break
        fi
        sleep 1
    done
else
    echo "✅ Backend is already running"
fi

# Check if frontend is running
if ! curl -s http://localhost:3000 > /dev/null; then
    echo "🌐 Starting Frontend Server..."
    cd frontend
    
    # Check if node_modules exists
    if [ ! -d node_modules ]; then
        echo "📦 Installing frontend dependencies..."
        npm install
    fi
    
    # Start frontend
    npm start &
    FRONTEND_PID=$!
    echo "✅ Frontend started with PID: $FRONTEND_PID"
    
    # Wait for frontend to be ready
    echo "⏳ Waiting for frontend to be ready..."
    for i in {1..30}; do
        if curl -s http://localhost:3000 > /dev/null; then
            echo "✅ Frontend is ready!"
            break
        fi
        sleep 1
    done
else
    echo "✅ Frontend is already running"
fi

echo ""
echo "🎉 AI Finance Advisor is now running!"
echo "=================================================="
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "🔐 Authentication Features:"
echo "   - User registration and login"
echo "   - Password reset functionality"
echo "   - Protected routes and endpoints"
echo "   - JWT token-based authentication"
echo ""
echo "🧪 Test the authentication system:"
echo "   python test_auth.py"
echo ""
echo "🛑 To stop the servers, press Ctrl+C"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping servers..."
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null
        echo "✅ Backend stopped"
    fi
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null
        echo "✅ Frontend stopped"
    fi
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Keep script running
wait
