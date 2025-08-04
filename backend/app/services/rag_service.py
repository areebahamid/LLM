import os
import pickle
import time
from typing import List, Dict, Any, Optional
import numpy as np
from pathlib import Path

import faiss
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

from app.core.config import settings

class RAGService:
    """Service for handling RAG (Retrieval-Augmented Generation) operations"""
    
    def __init__(self):
        self.embedding_model = SentenceTransformer(settings.embedding_model)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
            length_function=len,
        )
        self.faiss_index = None
        self.documents = []
        self._load_or_create_index()
    
    def _load_or_create_index(self):
        """Load existing FAISS index or create a new one"""
        index_path = Path(settings.faiss_index_path)
        docs_path = index_path.parent / "documents.pkl"
        
        if index_path.exists() and docs_path.exists():
            try:
                # Load existing index and documents
                self.faiss_index = faiss.read_index(str(index_path))
                with open(docs_path, 'rb') as f:
                    self.documents = pickle.load(f)
                print(f"Loaded existing FAISS index with {len(self.documents)} documents")
            except Exception as e:
                print(f"Error loading existing index: {e}")
                self._create_new_index()
        else:
            self._create_new_index()
    
    def _create_new_index(self):
        """Create a new FAISS index"""
        try:
            # Create a new FAISS index for the embedding dimension
            embedding_dim = self.embedding_model.get_sentence_embedding_dimension()
            self.faiss_index = faiss.IndexFlatIP(embedding_dim)  # Inner product for cosine similarity
            self.documents = []
            print(f"Created new FAISS index with dimension {embedding_dim}")
        except Exception as e:
            print(f"Error creating FAISS index: {e}")
            self.faiss_index = None
    
    def _save_index(self):
        """Save the FAISS index and documents to disk"""
        if self.faiss_index is None:
            return
        
        try:
            index_path = Path(settings.faiss_index_path)
            docs_path = index_path.parent / "documents.pkl"
            
            # Ensure directory exists
            index_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Save FAISS index
            faiss.write_index(self.faiss_index, str(index_path))
            
            # Save documents
            with open(docs_path, 'wb') as f:
                pickle.dump(self.documents, f)
            
            print(f"Saved FAISS index and {len(self.documents)} documents")
        except Exception as e:
            print(f"Error saving index: {e}")
    
    def add_documents(self, documents: List[Document]) -> bool:
        """Add documents to the knowledge base"""
        if self.faiss_index is None:
            print("FAISS index not initialized")
            return False
        
        try:
            # Split documents into chunks
            chunks = self.text_splitter.split_documents(documents)
            
            if not chunks:
                print("No chunks generated from documents")
                return False
            
            # Generate embeddings for chunks
            texts = [chunk.page_content for chunk in chunks]
            embeddings = self.embedding_model.encode(texts, show_progress_bar=True)
            
            # Normalize embeddings for cosine similarity
            faiss.normalize_L2(embeddings)
            
            # Add to FAISS index
            self.faiss_index.add(embeddings.astype('float32'))
            
            # Store document metadata
            for chunk in chunks:
                self.documents.append({
                    'content': chunk.page_content,
                    'metadata': chunk.metadata,
                    'source': chunk.metadata.get('source', 'unknown')
                })
            
            # Save updated index
            self._save_index()
            
            print(f"Added {len(chunks)} chunks to knowledge base")
            return True
            
        except Exception as e:
            print(f"Error adding documents: {e}")
            return False
    
    def search(self, query: str, top_k: int = None) -> List[Dict[str, Any]]:
        """Search for relevant documents using vector similarity"""
        if self.faiss_index is None or not self.documents:
            return []
        
        try:
            # Use default top_k if not specified
            if top_k is None:
                top_k = settings.top_k_results
            
            # Generate query embedding
            query_embedding = self.embedding_model.encode([query])
            faiss.normalize_L2(query_embedding)
            
            # Search in FAISS index
            scores, indices = self.faiss_index.search(
                query_embedding.astype('float32'), 
                min(top_k, len(self.documents))
            )
            
            # Return relevant documents with scores
            results = []
            for score, idx in zip(scores[0], indices[0]):
                if idx < len(self.documents):
                    results.append({
                        'content': self.documents[idx]['content'],
                        'metadata': self.documents[idx]['metadata'],
                        'source': self.documents[idx]['source'],
                        'score': float(score)
                    })
            
            return results
            
        except Exception as e:
            print(f"Error searching documents: {e}")
            return []
    
    def get_knowledge_base_info(self) -> Dict[str, Any]:
        """Get information about the knowledge base"""
        return {
            'total_documents': len(self.documents),
            'index_size': self.faiss_index.ntotal if self.faiss_index else 0,
            'embedding_model': settings.embedding_model,
            'chunk_size': settings.chunk_size,
            'chunk_overlap': settings.chunk_overlap,
            'index_path': settings.faiss_index_path
        }
    
    def clear_knowledge_base(self) -> bool:
        """Clear the entire knowledge base"""
        try:
            self._create_new_index()
            self._save_index()
            print("Knowledge base cleared")
            return True
        except Exception as e:
            print(f"Error clearing knowledge base: {e}")
            return False
    
    def add_text_documents(self, texts: List[str], metadata: List[Dict[str, Any]] = None) -> bool:
        """Add plain text documents to the knowledge base"""
        if metadata is None:
            metadata = [{'source': f'text_{i}'} for i in range(len(texts))]
        
        documents = []
        for text, meta in zip(texts, metadata):
            documents.append(Document(page_content=text, metadata=meta))
        
        return self.add_documents(documents)

# Create global instance
rag_service = RAGService() 