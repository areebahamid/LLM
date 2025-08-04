from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import time

from app.services.llm_service import llm_service
from app.services.rag_service import rag_service

router = APIRouter()

@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """Basic health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "service": "Student LLM Assistant API"
    }

@router.get("/health/detailed")
async def detailed_health_check() -> Dict[str, Any]:
    """Detailed health check including all services"""
    health_status = {
        "status": "healthy",
        "timestamp": time.time(),
        "services": {}
    }
    
    # Check LLM service
    try:
        ollama_status = await llm_service.check_ollama_status()
        health_status["services"]["llm"] = {
            "status": "healthy" if ollama_status["status"] == "running" else "unhealthy",
            "ollama_status": ollama_status
        }
    except Exception as e:
        health_status["services"]["llm"] = {
            "status": "error",
            "error": str(e)
        }
    
    # Check RAG service
    try:
        rag_info = rag_service.get_knowledge_base_info()
        health_status["services"]["rag"] = {
            "status": "healthy",
            "knowledge_base": rag_info
        }
    except Exception as e:
        health_status["services"]["rag"] = {
            "status": "error",
            "error": str(e)
        }
    
    # Overall status
    all_healthy = all(
        service.get("status") == "healthy" 
        for service in health_status["services"].values()
    )
    
    if not all_healthy:
        health_status["status"] = "degraded"
    
    return health_status

@router.get("/health/ollama")
async def ollama_health_check() -> Dict[str, Any]:
    """Check Ollama service status"""
    try:
        status = await llm_service.check_ollama_status()
        return {
            "service": "ollama",
            "status": status,
            "timestamp": time.time()
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Ollama service error: {str(e)}")

@router.get("/health/rag")
async def rag_health_check() -> Dict[str, Any]:
    """Check RAG service status"""
    try:
        info = rag_service.get_knowledge_base_info()
        return {
            "service": "rag",
            "status": "healthy",
            "knowledge_base": info,
            "timestamp": time.time()
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"RAG service error: {str(e)}") 