from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # API Configuration
    api_v1_str: str = "/api/v1"
    project_name: str = "Student LLM Assistant"
    
    # Ollama Configuration
    ollama_base_url: str = "http://localhost:11434"
    model_name: str = "llama2:7b"
    
    # FAISS Configuration
    faiss_index_path: str = "./data/faiss_index"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    # OpenAI Configuration (fallback)
    openai_api_key: Optional[str] = None
    
    # CORS Configuration
    cors_origins: list = ["http://localhost:3000", "http://localhost:5173"]
    
    # File Upload Configuration
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    allowed_file_types: list = [".txt", ".pdf", ".docx", ".md"]
    upload_dir: str = "./data/uploads"
    
    # RAG Configuration
    chunk_size: int = 1000
    chunk_overlap: int = 200
    top_k_results: int = 5
    
    # Chat Configuration
    max_tokens: int = 2048
    temperature: float = 0.7
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Create settings instance
settings = Settings()

# Ensure directories exist
os.makedirs(settings.upload_dir, exist_ok=True)
os.makedirs(os.path.dirname(settings.faiss_index_path), exist_ok=True) 