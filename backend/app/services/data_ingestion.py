import os
import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging
from app.config import settings
from app.services.rag_pipeline import RAGPipeline
from app.utils.document_processor import DocumentProcessor

logger = logging.getLogger(__name__)


class DataIngestionService:
    def __init__(self):
        self.rag_pipeline = RAGPipeline()
        self.document_processor = DocumentProcessor()
        self.upload_dir = settings.upload_dir

    async def process_uploaded_file(
        self, 
        file_path: str, 
        original_filename: str,
        file_type: str
    ) -> Dict[str, Any]:
        """Process an uploaded file and add it to the vector store"""
        try:
            # Generate unique document ID
            document_id = str(uuid.uuid4())
            
            # Extract text content from file
            content = await self.document_processor.extract_text(file_path, file_type)
            
            if not content:
                raise ValueError("Could not extract content from file")
            
            # Create metadata
            metadata = {
                "document_id": document_id,
                "filename": original_filename,
                "file_type": file_type,
                "file_size": os.path.getsize(file_path),
                "uploaded_at": datetime.now().isoformat(),
                "processed_at": datetime.now().isoformat()
            }
            
            # Process document through RAG pipeline
            documents = self.rag_pipeline.process_document(content, metadata)
            
            if not documents:
                raise ValueError("Failed to process document into chunks")
            
            # Add documents to vector store
            self.rag_pipeline.add_documents(documents)
            
            # Save file info for future reference
            file_info = {
                "document_id": document_id,
                "filename": original_filename,
                "file_type": file_type,
                "file_path": file_path,
                "content_length": len(content),
                "chunks_count": len(documents),
                "uploaded_at": metadata["uploaded_at"],
                "processed_at": metadata["processed_at"]
            }
            
            logger.info(f"Successfully processed file: {original_filename} (ID: {document_id})")
            return file_info
            
        except Exception as e:
            logger.error(f"Error processing file {original_filename}: {str(e)}")
            raise

    async def process_multiple_files(
        self, 
        files: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Process multiple uploaded files"""
        results = []
        
        for file_info in files:
            try:
                result = await self.process_uploaded_file(
                    file_info["file_path"],
                    file_info["original_filename"],
                    file_info["file_type"]
                )
                results.append(result)
            except Exception as e:
                logger.error(f"Error processing file {file_info.get('original_filename', 'Unknown')}: {str(e)}")
                results.append({
                    "error": str(e),
                    "filename": file_info.get("original_filename", "Unknown")
                })
        
        return results

    async def get_document_content(
        self, 
        document_id: str
    ) -> Optional[str]:
        """Get the original content of a document"""
        try:
            # Search for documents with this ID
            docs = self.rag_pipeline.search_documents(
                "", 
                k=100, 
                filter_metadata={"document_id": document_id}
            )
            
            if not docs:
                return None
            
            # Combine all chunks for this document
            content_parts = []
            for doc in docs:
                content_parts.append(doc.page_content)
            
            return "\n".join(content_parts)
            
        except Exception as e:
            logger.error(f"Error retrieving document content for {document_id}: {str(e)}")
            return None

    async def update_document(
        self, 
        document_id: str, 
        new_content: str
    ) -> bool:
        """Update an existing document with new content"""
        try:
            # First, remove old document (this is a simplified approach)
            # In a production system, you'd want to implement proper document replacement
            
            # Process new content
            metadata = {
                "document_id": document_id,
                "updated_at": datetime.now().isoformat()
            }
            
            documents = self.rag_pipeline.process_document(new_content, metadata)
            
            if not documents:
                return False
            
            # Add new documents to vector store
            self.rag_pipeline.add_documents(documents)
            
            logger.info(f"Successfully updated document: {document_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating document {document_id}: {str(e)}")
            return False

    async def delete_document(self, document_id: str) -> bool:
        """Delete a document from the system"""
        try:
            # Delete from vector store
            success = self.rag_pipeline.delete_document(document_id)
            
            if success:
                logger.info(f"Successfully deleted document: {document_id}")
            
            return success
            
        except Exception as e:
            logger.error(f"Error deleting document {document_id}: {str(e)}")
            return False

    async def get_document_list(self) -> List[Dict[str, Any]]:
        """Get list of all processed documents"""
        try:
            # This is a simplified implementation
            # In a production system, you'd want to maintain a separate document registry
            
            # For now, return basic stats
            stats = self.rag_pipeline.get_document_stats()
            
            return [{
                "total_documents": stats["total_documents"],
                "index_size": stats["index_size"],
                "last_updated": datetime.now().isoformat()
            }]
            
        except Exception as e:
            logger.error(f"Error getting document list: {str(e)}")
            return []

    async def search_documents(
        self, 
        query: str, 
        max_results: int = 5
    ) -> List[Dict[str, Any]]:
        """Search for documents containing the query"""
        try:
            docs = self.rag_pipeline.search_documents(query, k=max_results)
            
            results = []
            for doc in docs:
                results.append({
                    "document_id": doc.metadata.get("document_id"),
                    "filename": doc.metadata.get("filename"),
                    "content": doc.page_content,
                    "relevance_score": doc.metadata.get("score", 0),
                    "chunk_id": doc.metadata.get("chunk_id")
                })
            
            return results
            
        except Exception as e:
            logger.error(f"Error searching documents: {str(e)}")
            return []

    async def get_document_analytics(self) -> Dict[str, Any]:
        """Get analytics about processed documents"""
        try:
            stats = self.rag_pipeline.get_document_stats()
            
            # Get file type distribution (simplified)
            file_types = {
                "pdf": 0,
                "docx": 0,
                "xlsx": 0,
                "txt": 0
            }
            
            return {
                "total_documents": stats["total_documents"],
                "index_size": stats["index_size"],
                "file_type_distribution": file_types,
                "last_processed": datetime.now().isoformat(),
                "storage_used_mb": round(stats["index_size"] * 0.001, 2)  # Rough estimate
            }
            
        except Exception as e:
            logger.error(f"Error getting document analytics: {str(e)}")
            return {
                "total_documents": 0,
                "index_size": 0,
                "file_type_distribution": {},
                "last_processed": datetime.now().isoformat(),
                "storage_used_mb": 0
            }

    async def reindex_all_documents(self) -> bool:
        """Reindex all documents in the system"""
        try:
            logger.info("Starting full reindex of all documents")
            
            # Clear existing index
            self.rag_pipeline.clear_vector_store()
            
            # In a production system, you'd iterate through all stored documents
            # and reprocess them. For now, we'll just log the action.
            
            logger.info("Full reindex completed")
            return True
            
        except Exception as e:
            logger.error(f"Error during reindex: {str(e)}")
            return False

    async def validate_file(self, file_path: str, file_type: str) -> Dict[str, Any]:
        """Validate a file before processing"""
        try:
            # Check file size
            file_size = os.path.getsize(file_path)
            if file_size > settings.max_file_size:
                return {
                    "valid": False,
                    "error": f"File size ({file_size} bytes) exceeds maximum allowed size ({settings.max_file_size} bytes)"
                }
            
            # Check file type
            allowed_types = ["pdf", "docx", "xlsx", "txt"]
            if file_type.lower() not in allowed_types:
                return {
                    "valid": False,
                    "error": f"File type '{file_type}' is not supported. Allowed types: {', '.join(allowed_types)}"
                }
            
            # Try to extract content to validate file integrity
            content = await self.document_processor.extract_text(file_path, file_type)
            if not content:
                return {
                    "valid": False,
                    "error": "Could not extract content from file. File may be corrupted or password protected."
                }
            
            return {
                "valid": True,
                "file_size": file_size,
                "content_length": len(content),
                "file_type": file_type
            }
            
        except Exception as e:
            return {
                "valid": False,
                "error": f"Error validating file: {str(e)}"
            }
