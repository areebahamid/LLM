import asyncio
import time
from typing import Dict, Any, Optional, List, Union
import requests
from langchain_ollama import OllamaLLM
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.callbacks import CallbackManager
from langchain_core.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

from app.core.config import settings
from app.models.chat import ChatMessage, ModelInfo

class LLMService:
    """Service for handling LLM interactions with Ollama"""
    
    def __init__(self):
        self.ollama_base_url = settings.ollama_base_url
        self.model_name = settings.model_name
        self.llm = None
        self._initialize_llm()
    
    def _initialize_llm(self):
        """Initialize the Ollama LLM instance"""
        try:
            self.llm = OllamaLLM(
                base_url=self.ollama_base_url,
                model=self.model_name,
                temperature=settings.temperature,
                callback_manager=CallbackManager([StreamingStdOutCallbackHandler()])
            )
        except Exception as e:
            print(f"Failed to initialize Ollama LLM: {e}")
            self.llm = None
    
    async def generate_response(
        self, 
        message: str, 
        conversation_history: Optional[List[ChatMessage]] = None,
        model_params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Generate a response from the LLM"""
        start_time = time.time()
        
        if not self.llm:
            return {
                "response": "Sorry, the LLM service is currently unavailable. Please check if Ollama is running.",
                "model_used": "none",
                "processing_time": time.time() - start_time,
                "error": "LLM not initialized"
            }
        
        try:
            # Prepare conversation history for LangChain
            messages = []
            if conversation_history:
                for msg in conversation_history:
                    if msg.role == "user":
                        messages.append(HumanMessage(content=msg.content))
                    elif msg.role == "assistant":
                        messages.append(AIMessage(content=msg.content))
            
            # Add current message
            messages.append(HumanMessage(content=message))
            
            # Apply custom model parameters if provided
            if model_params:
                temp_llm = OllamaLLM(
                    base_url=self.ollama_base_url,
                    model=self.model_name,
                    **model_params
                )
                response: Any = await temp_llm.ainvoke(messages)
            else:
                response: Any = await self.llm.ainvoke(messages)
            
            processing_time = time.time() - start_time
            
            # Handle response content properly
            response_content = response.content if hasattr(response, 'content') else str(response)  # type: ignore
            
            return {
                "response": response_content,
                "model_used": self.model_name,
                "processing_time": processing_time,
                "tokens_used": None  # Ollama doesn't provide token count by default
            }
            
        except Exception as e:
            processing_time = time.time() - start_time
            return {
                "response": f"An error occurred while generating the response: {str(e)}",
                "model_used": self.model_name,
                "processing_time": processing_time,
                "error": str(e)
            }
    
    async def generate_streaming_response(
        self, 
        message: str, 
        conversation_history: Optional[List[ChatMessage]] = None,
        model_params: Optional[Dict[str, Any]] = None
    ):
        """Generate a streaming response from the LLM"""
        if not self.llm:
            yield {
                "chunk": "Sorry, the LLM service is currently unavailable.",
                "done": True,
                "model_used": "none",
                "error": "LLM not initialized"
            }
            return
        
        try:
            # Prepare conversation history
            messages = []
            if conversation_history:
                for msg in conversation_history:
                    if msg.role == "user":
                        messages.append(HumanMessage(content=msg.content))
                    elif msg.role == "assistant":
                        messages.append(AIMessage(content=msg.content))
            
            messages.append(HumanMessage(content=message))
            
            # Apply custom parameters
            if model_params:
                temp_llm = OllamaLLM(
                    base_url=self.ollama_base_url,
                    model=self.model_name,
                    **model_params
                )
                llm_to_use = temp_llm
            else:
                llm_to_use = self.llm
            
            # Stream the response
            async for chunk in llm_to_use.astream(messages):
                chunk_content = chunk.content if hasattr(chunk, 'content') else str(chunk)  # type: ignore
                if chunk_content:
                    yield {
                        "chunk": chunk_content,
                        "done": False,
                        "model_used": self.model_name
                    }
            
            yield {
                "chunk": "",
                "done": True,
                "model_used": self.model_name
            }
            
        except Exception as e:
            yield {
                "chunk": f"An error occurred: {str(e)}",
                "done": True,
                "model_used": self.model_name,
                "error": str(e)
            }
    
    async def get_available_models(self) -> List[ModelInfo]:
        """Get list of available Ollama models"""
        try:
            response = requests.get(f"{self.ollama_base_url}/api/tags")
            if response.status_code == 200:
                models_data = response.json()
                models = []
                for model in models_data.get("models", []):
                    models.append(ModelInfo(
                        name=model.get("name", ""),
                        provider="ollama",
                        context_length=None,
                        parameters=None,
                        is_available=True
                    ))
                return models
            else:
                return []
        except Exception as e:
            print(f"Error fetching available models: {e}")
            return []
    
    async def check_ollama_status(self) -> Dict[str, Any]:
        """Check if Ollama is running and accessible"""
        try:
            response = requests.get(f"{self.ollama_base_url}/api/tags", timeout=5)
            return {
                "status": "running" if response.status_code == 200 else "error",
                "status_code": response.status_code,
                "base_url": self.ollama_base_url
            }
        except requests.exceptions.RequestException as e:
            return {
                "status": "not_available",
                "error": str(e),
                "base_url": self.ollama_base_url
            }

# Create global instance
llm_service = LLMService() 