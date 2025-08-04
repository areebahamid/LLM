from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from typing import Dict, Any, List, Optional
import os
import aiofiles
from pathlib import Path
import uuid

from app.core.config import settings
from app.services.rag_service import rag_service
from langchain.schema import Document

router = APIRouter()

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    description: Optional[str] = Form(None)
) -> Dict[str, Any]:
    """Upload a document to the knowledge base"""
    try:
        # Validate file type
        file_extension = Path(file.filename).suffix.lower()
        if file_extension not in settings.allowed_file_types:
            raise HTTPException(
                status_code=400,
                detail=f"File type {file_extension} not allowed. Allowed types: {settings.allowed_file_types}"
            )
        
        # Validate file size
        if file.size and file.size > settings.max_file_size:
            raise HTTPException(
                status_code=400,
                detail=f"File size {file.size} exceeds maximum allowed size of {settings.max_file_size}"
            )
        
        # Create unique filename
        unique_filename = f"{uuid.uuid4()}_{file.filename}"
        file_path = Path(settings.upload_dir) / unique_filename
        
        # Save file
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        # Process document based on file type
        success = await process_document(file_path, file_extension, description)
        
        if success:
            return {
                "message": "Document uploaded and processed successfully",
                "filename": unique_filename,
                "original_name": file.filename,
                "size": len(content),
                "description": description
            }
        else:
            # Clean up file if processing failed
            os.remove(file_path)
            raise HTTPException(status_code=500, detail="Failed to process document")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading document: {str(e)}")

@router.post("/text")
async def add_text_document(
    text: str = Form(...),
    source: str = Form("manual_input"),
    description: Optional[str] = Form(None)
) -> Dict[str, Any]:
    """Add plain text to the knowledge base"""
    try:
        if not text.strip():
            raise HTTPException(status_code=400, detail="Text cannot be empty")
        
        # Create metadata
        metadata = {
            "source": source,
            "description": description,
            "type": "text"
        }
        
        # Add to knowledge base
        success = rag_service.add_text_documents([text], [metadata])
        
        if success:
            return {
                "message": "Text added to knowledge base successfully",
                "source": source,
                "description": description,
                "text_length": len(text)
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to add text to knowledge base")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding text: {str(e)}")

@router.get("/list")
async def list_documents() -> Dict[str, Any]:
    """List all documents in the knowledge base"""
    try:
        info = rag_service.get_knowledge_base_info()
        
        # Get uploaded files
        upload_dir = Path(settings.upload_dir)
        uploaded_files = []
        if upload_dir.exists():
            for file_path in upload_dir.iterdir():
                if file_path.is_file():
                    uploaded_files.append({
                        "filename": file_path.name,
                        "size": file_path.stat().st_size,
                        "modified": file_path.stat().st_mtime
                    })
        
        return {
            "knowledge_base": info,
            "uploaded_files": uploaded_files,
            "total_files": len(uploaded_files)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing documents: {str(e)}")

@router.get("/download/{filename}")
async def download_document(filename: str):
    """Download a specific document"""
    try:
        file_path = Path(settings.upload_dir) / filename
        
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found")
        
        return FileResponse(
            path=file_path,
            filename=filename,
            media_type='application/octet-stream'
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error downloading file: {str(e)}")

@router.delete("/{filename}")
async def delete_document(filename: str) -> Dict[str, Any]:
    """Delete a specific document"""
    try:
        file_path = Path(settings.upload_dir) / filename
        
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found")
        
        # Remove file
        os.remove(file_path)
        
        return {
            "message": "Document deleted successfully",
            "filename": filename
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting file: {str(e)}")

async def process_document(file_path: Path, file_extension: str, description: Optional[str] = None) -> bool:
    """Process uploaded document and add to knowledge base"""
    try:
        # Read file content based on type
        if file_extension == ".txt":
            async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
                content = await f.read()
        elif file_extension == ".md":
            async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
                content = await f.read()
        else:
            # For other file types, you might want to add more sophisticated processing
            # (e.g., PDF parsing, DOCX parsing, etc.)
            raise HTTPException(
                status_code=400,
                detail=f"File type {file_extension} processing not implemented yet"
            )
        
        # Create metadata
        metadata = {
            "source": str(file_path.name),
            "description": description,
            "type": file_extension[1:],  # Remove the dot
            "file_path": str(file_path)
        }
        
        # Add to knowledge base
        success = rag_service.add_text_documents([content], [metadata])
        
        return success
        
    except Exception as e:
        print(f"Error processing document {file_path}: {e}")
        return False 