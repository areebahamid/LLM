from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class ChatMessage(BaseModel):
    """Individual chat message model"""
    role: str = Field(..., description="Role of the message sender (user/assistant)")
    content: str = Field(..., description="Content of the message")
    timestamp: Optional[datetime] = Field(default_factory=datetime.now)

class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    message: str = Field(..., description="User's message", min_length=1, max_length=5000)
    conversation_history: Optional[List[ChatMessage]] = Field(
        default=[], 
        description="Previous conversation messages"
    )
    use_rag: bool = Field(default=True, description="Whether to use RAG for enhanced responses")
    model_params: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Optional model parameters (temperature, max_tokens, etc.)"
    )

class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    response: str = Field(..., description="Assistant's response")
    sources: Optional[List[Dict[str, Any]]] = Field(
        default=None,
        description="Sources used for RAG response"
    )
    model_used: str = Field(..., description="Name of the model used")
    processing_time: float = Field(..., description="Time taken to process the request")
    tokens_used: Optional[int] = Field(default=None, description="Number of tokens used")
    conversation_id: Optional[str] = Field(default=None, description="Unique conversation identifier")

class ChatStreamResponse(BaseModel):
    """Streaming response model for real-time chat"""
    chunk: str = Field(..., description="Partial response chunk")
    done: bool = Field(default=False, description="Whether the response is complete")
    sources: Optional[List[Dict[str, Any]]] = Field(default=None)
    model_used: Optional[str] = Field(default=None)

class Conversation(BaseModel):
    """Complete conversation model"""
    id: str = Field(..., description="Unique conversation identifier")
    title: str = Field(..., description="Conversation title")
    messages: List[ChatMessage] = Field(default=[], description="All messages in the conversation")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    metadata: Optional[Dict[str, Any]] = Field(default=None)

class ModelInfo(BaseModel):
    """Model information model"""
    name: str = Field(..., description="Model name")
    provider: str = Field(..., description="Model provider (ollama, openai, etc.)")
    context_length: Optional[int] = Field(default=None, description="Maximum context length")
    parameters: Optional[int] = Field(default=None, description="Number of parameters")
    is_available: bool = Field(..., description="Whether the model is available") 