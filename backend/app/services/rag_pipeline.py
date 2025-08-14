from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from app.config import settings
from typing import List, Dict, Any, Optional
import os
import pickle
import logging

logger = logging.getLogger(__name__)


class RAGPipeline:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name=settings.embedding_model,
            model_kwargs={'device': 'cpu'}
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        self.vector_store = None
        self.load_vector_store()

    def load_vector_store(self):
        """Load existing vector store or create new one"""
        try:
            vector_store_path = os.path.join(settings.vector_db_path, "faiss_index")
            if os.path.exists(vector_store_path):
                self.vector_store = FAISS.load_local(
                    vector_store_path, 
                    self.embeddings
                )
                logger.info("Loaded existing vector store")
            else:
                # Create empty vector store
                self.vector_store = FAISS.from_texts(
                    ["Initial document"], 
                    self.embeddings
                )
                logger.info("Created new vector store")
        except Exception as e:
            logger.error(f"Error loading vector store: {str(e)}")
            # Create empty vector store as fallback
            self.vector_store = FAISS.from_texts(
                ["Initial document"], 
                self.embeddings
            )

    def save_vector_store(self):
        """Save vector store to disk"""
        try:
            vector_store_path = os.path.join(settings.vector_db_path, "faiss_index")
            self.vector_store.save_local(vector_store_path)
            logger.info("Vector store saved successfully")
        except Exception as e:
            logger.error(f"Error saving vector store: {str(e)}")

    def process_document(self, content: str, metadata: Dict[str, Any]) -> List[Document]:
        """Process document content and create chunks"""
        try:
            # Split text into chunks
            chunks = self.text_splitter.split_text(content)
            
            # Create documents with metadata
            documents = []
            for i, chunk in enumerate(chunks):
                doc = Document(
                    page_content=chunk,
                    metadata={
                        **metadata,
                        "chunk_id": i,
                        "chunk_size": len(chunk)
                    }
                )
                documents.append(doc)
            
            logger.info(f"Processed document into {len(documents)} chunks")
            return documents
            
        except Exception as e:
            logger.error(f"Error processing document: {str(e)}")
            return []

    def add_documents(self, documents: List[Document]):
        """Add documents to vector store"""
        try:
            if self.vector_store is None:
                self.load_vector_store()
            
            # Add documents to vector store
            self.vector_store.add_documents(documents)
            
            # Save updated vector store
            self.save_vector_store()
            
            logger.info(f"Added {len(documents)} documents to vector store")
            
        except Exception as e:
            logger.error(f"Error adding documents to vector store: {str(e)}")

    def search_documents(
        self, 
        query: str, 
        k: int = 5,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> List[Document]:
        """Search for relevant documents"""
        try:
            if self.vector_store is None:
                return []
            
            # Perform similarity search
            if filter_metadata:
                docs = self.vector_store.similarity_search(
                    query, 
                    k=k,
                    filter=filter_metadata
                )
            else:
                docs = self.vector_store.similarity_search(query, k=k)
            
            logger.info(f"Found {len(docs)} relevant documents for query: {query[:50]}...")
            return docs
            
        except Exception as e:
            logger.error(f"Error searching documents: {str(e)}")
            return []

    def get_context_for_query(
        self, 
        query: str, 
        max_chunks: int = 3
    ) -> str:
        """Get relevant context for a query"""
        try:
            # Search for relevant documents
            relevant_docs = self.search_documents(query, k=max_chunks)
            
            if not relevant_docs:
                return ""
            
            # Combine relevant content
            context_parts = []
            for doc in relevant_docs:
                context_parts.append(f"Document: {doc.metadata.get('filename', 'Unknown')}")
                context_parts.append(f"Content: {doc.page_content}")
                context_parts.append("---")
            
            context = "\n".join(context_parts)
            logger.info(f"Generated context with {len(relevant_docs)} document chunks")
            return context
            
        except Exception as e:
            logger.error(f"Error generating context: {str(e)}")
            return ""

    def delete_document(self, document_id: str) -> bool:
        """Delete a document from vector store"""
        try:
            # Note: FAISS doesn't support direct deletion
            # This would require rebuilding the index without the document
            # For now, we'll mark it as deleted in metadata
            logger.warning("Document deletion not fully implemented for FAISS")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting document: {str(e)}")
            return False

    def get_document_stats(self) -> Dict[str, Any]:
        """Get statistics about the vector store"""
        try:
            if self.vector_store is None:
                return {"total_documents": 0, "index_size": 0}
            
            # Get basic stats
            stats = {
                "total_documents": len(self.vector_store.docstore._dict),
                "index_size": self.vector_store.index.ntotal if hasattr(self.vector_store.index, 'ntotal') else 0
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting document stats: {str(e)}")
            return {"total_documents": 0, "index_size": 0}

    def clear_vector_store(self):
        """Clear all documents from vector store"""
        try:
            self.vector_store = FAISS.from_texts(
                ["Initial document"], 
                self.embeddings
            )
            self.save_vector_store()
            logger.info("Vector store cleared successfully")
            
        except Exception as e:
            logger.error(f"Error clearing vector store: {str(e)}")
