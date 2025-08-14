#!/bin/bash

# AI Finance Advisor Setup Script
echo "🚀 Setting up AI Finance Advisor Application..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python 3.9+ is installed
check_python() {
    print_status "Checking Python version..."
    if command -v python3 &> /dev/null; then
        python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
        print_success "Python $python_version found"
    else
        print_error "Python 3.9+ is required but not installed"
        exit 1
    fi
}

# Check if Node.js is installed
check_node() {
    print_status "Checking Node.js version..."
    if command -v node &> /dev/null; then
        node_version=$(node --version)
        print_success "Node.js $node_version found"
    else
        print_error "Node.js 16+ is required but not installed"
        exit 1
    fi
}

# Setup backend
setup_backend() {
    print_status "Setting up backend..."
    
    cd backend
    
    # Create virtual environment
    print_status "Creating Python virtual environment..."
    python3 -m venv venv
    
    # Activate virtual environment
    print_status "Activating virtual environment..."
    source venv/bin/activate
    
    # Upgrade pip
    print_status "Upgrading pip..."
    pip install --upgrade pip
    
    # Install dependencies
    print_status "Installing Python dependencies..."
    pip install -r requirements.txt
    
    # Create necessary directories
    print_status "Creating data directories..."
    mkdir -p data/documents
    mkdir -p data/embeddings
    mkdir -p logs
    
    # Copy environment file
    if [ ! -f .env ]; then
        print_status "Creating .env file from template..."
        cp env.example .env
        print_warning "Please edit backend/.env with your API keys"
    fi
    
    cd ..
    print_success "Backend setup completed"
}

# Setup frontend
setup_frontend() {
    print_status "Setting up frontend..."
    
    cd frontend
    
    # Install dependencies
    print_status "Installing Node.js dependencies..."
    npm install
    
    cd ..
    print_success "Frontend setup completed"
}

# Create start scripts
create_start_scripts() {
    print_status "Creating start scripts..."
    
    # Backend start script
    cat > start_backend.sh << 'EOF'
#!/bin/bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
EOF
    chmod +x start_backend.sh
    
    # Frontend start script
    cat > start_frontend.sh << 'EOF'
#!/bin/bash
cd frontend
npm start
EOF
    chmod +x start_frontend.sh
    
    # Combined start script
    cat > start_all.sh << 'EOF'
#!/bin/bash
echo "Starting AI Finance Advisor..."

# Start backend in background
echo "Starting backend..."
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Start frontend
echo "Starting frontend..."
cd ../frontend
npm start &
FRONTEND_PID=$!

# Function to cleanup on exit
cleanup() {
    echo "Stopping services..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    exit 0
}

# Trap Ctrl+C and call cleanup
trap cleanup SIGINT

# Wait for both processes
wait
EOF
    chmod +x start_all.sh
    
    print_success "Start scripts created"
}

# Main setup function
main() {
    print_status "Starting AI Finance Advisor setup..."
    
    # Check prerequisites
    check_python
    check_node
    
    # Setup components
    setup_backend
    setup_frontend
    create_start_scripts
    
    print_success "🎉 Setup completed successfully!"
    echo ""
    print_status "Next steps:"
    echo "1. Edit backend/.env with your API keys:"
    echo "   - GOOGLE_GEMINI_API_KEY (required)"
    echo "   - ALPHA_VANTAGE_API_KEY (optional)"
    echo "   - COINGECKO_API_KEY (optional)"
    echo ""
    echo "2. Start the application:"
    echo "   - Backend only: ./start_backend.sh"
    echo "   - Frontend only: ./start_frontend.sh"
    echo "   - Both: ./start_all.sh"
    echo ""
    echo "3. Access the application:"
    echo "   - Frontend: http://localhost:3000"
    echo "   - Backend API: http://localhost:8000"
    echo "   - API Docs: http://localhost:8000/docs"
    echo ""
    print_warning "Make sure to set up your API keys before starting the application!"
}

# Run main function
main
