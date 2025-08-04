from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
from dotenv import load_dotenv

from app.api.routes import chat, health, documents
from app.core.config import settings

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Student LLM Assistant API",
    description="A real-time LLM assistant for students using RAG + LangChain + FastAPI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(documents.router, prefix="/api/documents", tags=["documents"])

# Mount static files for uploaded documents
if os.path.exists("data/uploads"):
    app.mount("/uploads", StaticFiles(directory="data/uploads"), name="uploads")

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Student LLM Assistant API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/health"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 