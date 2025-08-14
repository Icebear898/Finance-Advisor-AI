# AI Finance Advisor

A comprehensive AI-powered financial advisory application that provides personalized financial advice, investment suggestions, tax planning, document analysis, and live market updates.

## Features

- **Personal Finance Advice**: Budgeting, savings, loan EMI calculations
- **Investment Suggestions**: Stock analysis, mutual fund recommendations, gold investment
- **Tax Planning**: Indian tax laws, Sections 80C, 80D optimization
- **Document Analysis**: PDF, Excel, and report analysis with insights
- **Live Market Updates**: Real-time stock prices, crypto rates, RBI interest rates

## Tech Stack

- **Backend**: FastAPI, LangChain, Google Gemini API
- **Frontend**: React, TypeScript, Tailwind CSS
- **Vector Database**: FAISS (local) / Pinecone (cloud)
- **Finance APIs**: Alpha Vantage, CoinGecko, RBI APIs
- **Document Processing**: PyPDF2, openpyxl, langchain-community

## Project Structure

```
FinanceBOT/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── chat.py
│   │   │   └── finance.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── rag_pipeline.py
│   │   │   ├── data_ingestion.py
│   │   │   ├── finance_api.py
│   │   │   └── gemini_service.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── routes/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── chat.py
│   │   │   │   ├── documents.py
│   │   │   │   └── finance.py
│   │   │   └── middleware.py
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── document_processor.py
│   │       └── helpers.py
│   ├── data/
│   │   ├── documents/
│   │   └── embeddings/
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── public/
│   │   ├── index.html
│   │   └── favicon.ico
│   ├── src/
│   │   ├── components/
│   │   │   ├── Chat/
│   │   │   ├── Dashboard/
│   │   │   ├── Documents/
│   │   │   └── Common/
│   │   ├── services/
│   │   ├── types/
│   │   ├── utils/
│   │   ├── App.tsx
│   │   └── index.tsx
│   ├── package.json
│   ├── tsconfig.json
│   └── tailwind.config.js
├── requirements.txt
└── README.md
```

## Setup Instructions

### Prerequisites

- Python 3.9+
- Node.js 16+
- Google Gemini API key
- Alpha Vantage API key (optional)
- CoinGecko API key (optional)

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

5. Run the backend:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start development server:
```bash
npm start
```

## API Endpoints

### Chat Endpoints
- `POST /api/chat` - Send message to AI advisor
- `GET /api/chat/history` - Get chat history

### Document Endpoints
- `POST /api/documents/upload` - Upload and process documents
- `GET /api/documents/list` - List processed documents
- `DELETE /api/documents/{doc_id}` - Delete document

### Finance Endpoints
- `GET /api/finance/stocks/{symbol}` - Get stock data
- `GET /api/finance/crypto/{coin}` - Get crypto data
- `GET /api/finance/rbi-rates` - Get RBI interest rates
- `POST /api/finance/calculate-emi` - Calculate loan EMI

## Usage Examples

### Personal Finance Query
```
"My salary is ₹50,000 and EMI ₹15,000. How can I save more?"
```

### Investment Query
```
"Should I invest in HDFC Bank stocks? What's the current market sentiment?"
```

### Tax Planning Query
```
"What are the best tax-saving investments under Section 80C for FY 2024-25?"
```

## Production Deployment

### Backend (Docker)
```bash
docker build -t finance-advisor-backend .
docker run -p 8000:8000 finance-advisor-backend
```

### Frontend (Build)
```bash
cd frontend
npm run build
# Serve the build folder with nginx or similar
```

## Security Features

- API key authentication
- CORS configuration
- Input validation and sanitization
- Rate limiting
- Secure file upload handling

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details
