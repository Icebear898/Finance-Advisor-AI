from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from loguru import logger
import sys

from app.config import settings
from app.api.routes import chat, documents, finance, auth

# Configure logging
logging.basicConfig(level=logging.INFO)
logger.remove()
logger.add(sys.stdout, level=settings.log_level)
logger.add(settings.log_file, rotation="10 MB", retention="7 days", level=settings.log_level)

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="AI-powered Financial Advisory System with RAG capabilities",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(chat.router)
app.include_router(documents.router)
app.include_router(finance.router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AI Finance Advisor API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": "2024-01-01T00:00:00Z",
        "version": "1.0.0"
    }


@app.get("/api/status")
async def api_status():
    """API status and configuration"""
    return {
        "app_name": settings.app_name,
        "environment": settings.environment,
        "debug": settings.debug,
        "api_keys_configured": {
            "google_gemini": bool(settings.google_gemini_api_key),
            "alpha_vantage": bool(settings.alpha_vantage_api_key),
            "coingecko": bool(settings.coingecko_api_key)
        },
        "features": {
            "chat": True,
            "document_analysis": True,
            "market_data": True,
            "financial_calculators": True,
            "rag_pipeline": True
        }
    }


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Global HTTP exception handler"""
    logger.error(f"HTTP Exception: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "timestamp": "2024-01-01T00:00:00Z"
        }
    )


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled Exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred",
            "timestamp": "2024-01-01T00:00:00Z"
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )
