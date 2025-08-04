from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from typing import Dict, Any, List
import json
import uuid

from app.models.chat import ChatRequest, ChatResponse, ChatStreamResponse, ModelInfo
from app.services.llm_service import llm_service
from app.services.rag_service import rag_service

router = APIRouter()

@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """Generate a response using LLM with optional RAG enhancement"""
    try:
        # If RAG is enabled, search for relevant documents
        sources = None
        enhanced_message = request.message
        
        if request.use_rag:
            relevant_docs = rag_service.search(request.message)
            if relevant_docs:
                # Create context from relevant documents
                context = "\n\n".join([
                    f"Source: {doc['source']}\nContent: {doc['content']}"
                    for doc in relevant_docs[:3]  # Use top 3 sources
                ])
                
                enhanced_message = f"""Based on the following context, please answer the user's question:

Context:
{context}

User Question: {request.message}

Please provide a comprehensive answer based on the context provided. If the context doesn't contain enough information to answer the question, please say so."""
                
                sources = [
                    {
                        "content": doc["content"][:200] + "...",
                        "source": doc["source"],
                        "score": doc["score"]
                    }
                    for doc in relevant_docs[:3]
                ]
        
        # Generate response from LLM
        llm_response = await llm_service.generate_response(
            message=enhanced_message,
            conversation_history=request.conversation_history,
            model_params=request.model_params
        )
        
        # Create response
        response = ChatResponse(
            response=llm_response["response"],
            sources=sources,
            model_used=llm_response["model_used"],
            processing_time=llm_response["processing_time"],
            tokens_used=llm_response.get("tokens_used"),
            conversation_id=str(uuid.uuid4())
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")

@router.post("/stream")
async def chat_stream(request: ChatRequest):
    """Generate a streaming response using LLM with optional RAG enhancement"""
    async def generate_stream():
        try:
            # If RAG is enabled, search for relevant documents
            sources = None
            enhanced_message = request.message
            
            if request.use_rag:
                relevant_docs = rag_service.search(request.message)
                if relevant_docs:
                    # Create context from relevant documents
                    context = "\n\n".join([
                        f"Source: {doc['source']}\nContent: {doc['content']}"
                        for doc in relevant_docs[:3]
                    ])
                    
                    enhanced_message = f"""Based on the following context, please answer the user's question:

Context:
{context}

User Question: {request.message}

Please provide a comprehensive answer based on the context provided. If the context doesn't contain enough information to answer the question, please say so."""
                    
                    sources = [
                        {
                            "content": doc["content"][:200] + "...",
                            "source": doc["source"],
                            "score": doc["score"]
                        }
                        for doc in relevant_docs[:3]
                    ]
            
            # Stream response from LLM
            async for chunk in llm_service.generate_streaming_response(
                message=enhanced_message,
                conversation_history=request.conversation_history,
                model_params=request.model_params
            ):
                # Add sources to the final chunk
                if chunk.get("done", False):
                    chunk["sources"] = sources
                
                yield f"data: {json.dumps(chunk)}\n\n"
            
        except Exception as e:
            error_chunk = {
                "chunk": f"Error: {str(e)}",
                "done": True,
                "error": str(e)
            }
            yield f"data: {json.dumps(error_chunk)}\n\n"
    
    return StreamingResponse(
        generate_stream(),
        media_type="text/plain",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"}
    )

@router.get("/models", response_model=List[ModelInfo])
async def get_available_models() -> List[ModelInfo]:
    """Get list of available LLM models"""
    try:
        models = await llm_service.get_available_models()
        return models
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching models: {str(e)}")

@router.get("/search")
async def search_knowledge_base(query: str, top_k: int = 5) -> Dict[str, Any]:
    """Search the knowledge base for relevant documents"""
    try:
        results = rag_service.search(query, top_k=top_k)
        return {
            "query": query,
            "results": results,
            "total_results": len(results)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching knowledge base: {str(e)}")

@router.get("/knowledge-base/info")
async def get_knowledge_base_info() -> Dict[str, Any]:
    """Get information about the knowledge base"""
    try:
        info = rag_service.get_knowledge_base_info()
        return info
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching knowledge base info: {str(e)}")

@router.delete("/knowledge-base")
async def clear_knowledge_base() -> Dict[str, Any]:
    """Clear the entire knowledge base"""
    try:
        success = rag_service.clear_knowledge_base()
        if success:
            return {"message": "Knowledge base cleared successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to clear knowledge base")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing knowledge base: {str(e)}") 