from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends
from typing import List, Optional
import logging
import os
import shutil
from datetime import datetime
from app.models.auth import User
from app.services.data_ingestion import DataIngestionService
from app.utils.helpers import sanitize_filename, format_file_size
from app.config import settings
from app.dependencies.auth import get_current_active_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/documents", tags=["documents"])

# Initialize service
data_ingestion_service = DataIngestionService()


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    description: Optional[str] = Form(None),
    current_user: User = Depends(get_current_active_user)
):
    """Upload and process a document"""
    try:
        # Validate file
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        # Get file extension
        file_extension = os.path.splitext(file.filename)[1].lower()
        file_type = file_extension[1:] if file_extension else ""
        
        # Validate file type
        allowed_types = ["pdf", "docx", "xlsx", "xls", "txt"]
        if file_type not in allowed_types:
            raise HTTPException(
                status_code=400, 
                detail=f"File type '{file_type}' not supported. Allowed types: {', '.join(allowed_types)}"
            )
        
        # Validate file size
        if file.size > settings.max_file_size:
            raise HTTPException(
                status_code=400,
                detail=f"File size ({format_file_size(file.size)}) exceeds maximum allowed size ({format_file_size(settings.max_file_size)})"
            )
        
        # Sanitize filename
        safe_filename = sanitize_filename(file.filename)
        
        # Create unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_filename = f"{timestamp}_{safe_filename}"
        file_path = os.path.join(settings.upload_dir, unique_filename)
        
        # Save file
        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
        except Exception as e:
            logger.error(f"Error saving file: {str(e)}")
            raise HTTPException(status_code=500, detail="Error saving file")
        
        # Validate file integrity
        validation_result = await data_ingestion_service.validate_file(file_path, file_type)
        if not validation_result["valid"]:
            # Clean up file
            os.remove(file_path)
            raise HTTPException(status_code=400, detail=validation_result["error"])
        
        # Process file
        try:
            result = await data_ingestion_service.process_uploaded_file(
                file_path=file_path,
                original_filename=file.filename,
                file_type=file_type
            )
            
            # Add description if provided
            if description:
                result["description"] = description
            
            logger.info(f"Successfully uploaded and processed: {file.filename}")
            return {
                "message": "Document uploaded and processed successfully",
                "document": result
            }
            
        except Exception as e:
            # Clean up file on processing error
            os.remove(file_path)
            logger.error(f"Error processing file: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading document: {str(e)}")
        raise HTTPException(status_code=500, detail="Error uploading document")


@router.get("/list")
async def list_documents():
    """Get list of all processed documents"""
    try:
        documents = await data_ingestion_service.get_document_list()
        return {
            "documents": documents,
            "total_count": len(documents)
        }
        
    except Exception as e:
        logger.error(f"Error listing documents: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving documents")


@router.get("/{document_id}")
async def get_document(document_id: str):
    """Get document details and content"""
    try:
        # Get document content
        content = await data_ingestion_service.get_document_content(document_id)
        
        if content is None:
            raise HTTPException(status_code=404, detail="Document not found")
        
        return {
            "document_id": document_id,
            "content": content,
            "content_length": len(content),
            "retrieved_at": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving document {document_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving document")


@router.delete("/{document_id}")
async def delete_document(document_id: str):
    """Delete a document"""
    try:
        success = await data_ingestion_service.delete_document(document_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Document not found")
        
        return {"message": "Document deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting document {document_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error deleting document")


@router.post("/search")
async def search_documents(query: str, max_results: int = 5):
    """Search for documents containing the query"""
    try:
        if not query.strip():
            raise HTTPException(status_code=400, detail="Search query cannot be empty")
        
        results = await data_ingestion_service.search_documents(query, max_results)
        
        return {
            "query": query,
            "results": results,
            "total_results": len(results),
            "searched_at": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error searching documents: {str(e)}")
        raise HTTPException(status_code=500, detail="Error searching documents")


@router.get("/analytics/summary")
async def get_document_analytics():
    """Get analytics about processed documents"""
    try:
        analytics = await data_ingestion_service.get_document_analytics()
        
        return {
            "analytics": analytics,
            "generated_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting document analytics: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving analytics")


@router.post("/reindex")
async def reindex_documents():
    """Reindex all documents in the system"""
    try:
        success = await data_ingestion_service.reindex_all_documents()
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to reindex documents")
        
        return {"message": "Documents reindexed successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error reindexing documents: {str(e)}")
        raise HTTPException(status_code=500, detail="Error reindexing documents")


@router.post("/validate")
async def validate_document(file: UploadFile = File(...)):
    """Validate a document before processing"""
    try:
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        # Get file extension
        file_extension = os.path.splitext(file.filename)[1].lower()
        file_type = file_extension[1:] if file_extension else ""
        
        # Create temporary file for validation
        temp_filename = f"temp_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{sanitize_filename(file.filename)}"
        temp_path = os.path.join(settings.upload_dir, temp_filename)
        
        try:
            # Save file temporarily
            with open(temp_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            # Validate file
            validation_result = await data_ingestion_service.validate_file(temp_path, file_type)
            
            return {
                "validation_result": validation_result,
                "filename": file.filename,
                "file_type": file_type,
                "file_size": file.size
            }
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.remove(temp_path)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error validating document: {str(e)}")
        raise HTTPException(status_code=500, detail="Error validating document")
