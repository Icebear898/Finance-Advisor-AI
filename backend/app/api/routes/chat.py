from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
import logging
from app.models.chat import ChatRequest, ChatResponse, ChatMessage, MessageRole
from app.services.gemini_service import GeminiService
from app.services.rag_pipeline import RAGPipeline
from app.utils.helpers import parse_financial_query, generate_session_id
from datetime import datetime

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/chat", tags=["chat"])

# Initialize services
gemini_service = GeminiService()
rag_pipeline = RAGPipeline()

# In-memory storage for chat sessions (in production, use a database)
chat_sessions = {}


@router.post("/", response_model=ChatResponse)
async def send_message(request: ChatRequest):
    """Send a message to the AI Finance Advisor"""
    try:
        # Parse the financial query to extract context
        query_context = parse_financial_query(request.message)
        
        # Get relevant document context if document IDs are provided
        document_context = ""
        if request.document_ids:
            for doc_id in request.document_ids:
                doc_content = await get_document_content(doc_id)
                if doc_content:
                    document_context += f"\nDocument {doc_id}:\n{doc_content}\n"
        
        # Get relevant context from vector store
        rag_context = rag_pipeline.get_context_for_query(request.message)
        
        # Combine all context
        full_context = ""
        if document_context:
            full_context += f"User Documents:\n{document_context}\n\n"
        if rag_context:
            full_context += f"Relevant Information:\n{rag_context}\n\n"
        if query_context:
            full_context += f"Query Analysis:\n{query_context}\n\n"
        
        # Generate AI response
        ai_response = await gemini_service.generate_response(
            user_message=request.message,
            context=query_context,
            document_content=full_context if full_context else None
        )
        
        # Create response
        response = ChatResponse(
            message=ai_response,
            sources=[] if not rag_context else [{"type": "document", "content": rag_context[:200] + "..."}],
            suggestions=generate_suggestions(query_context["query_type"]),
            timestamp=datetime.now()
        )
        
        # Store in session (simplified - in production use proper session management)
        session_id = generate_session_id()
        if session_id not in chat_sessions:
            chat_sessions[session_id] = []
        
        # Add user message
        chat_sessions[session_id].append(ChatMessage(
            role=MessageRole.USER,
            content=request.message,
            timestamp=datetime.now()
        ))
        
        # Add AI response
        chat_sessions[session_id].append(ChatMessage(
            role=MessageRole.ASSISTANT,
            content=ai_response,
            timestamp=datetime.now()
        ))
        
        logger.info(f"Generated response for query: {request.message[:50]}...")
        return response
        
    except Exception as e:
        logger.error(f"Error processing chat message: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing your request")


@router.get("/history/{session_id}")
async def get_chat_history(session_id: str):
    """Get chat history for a session"""
    try:
        if session_id not in chat_sessions:
            return {"messages": []}
        
        return {"messages": chat_sessions[session_id]}
        
    except Exception as e:
        logger.error(f"Error retrieving chat history: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving chat history")


@router.delete("/history/{session_id}")
async def clear_chat_history(session_id: str):
    """Clear chat history for a session"""
    try:
        if session_id in chat_sessions:
            del chat_sessions[session_id]
        
        return {"message": "Chat history cleared successfully"}
        
    except Exception as e:
        logger.error(f"Error clearing chat history: {str(e)}")
        raise HTTPException(status_code=500, detail="Error clearing chat history")


@router.post("/investment-advice")
async def get_investment_advice(user_profile: dict):
    """Get personalized investment advice"""
    try:
        # Validate required fields
        required_fields = ["age", "income", "risk_tolerance", "investment_horizon"]
        for field in required_fields:
            if field not in user_profile:
                raise HTTPException(status_code=400, detail=f"Missing required field: {field}")
        
        # Generate investment advice
        advice = await gemini_service.generate_investment_advice(
            user_profile=user_profile,
            investment_goal=user_profile.get("investment_goal", "Wealth creation")
        )
        
        return {
            "advice": advice,
            "user_profile": user_profile,
            "generated_at": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating investment advice: {str(e)}")
        raise HTTPException(status_code=500, detail="Error generating investment advice")


@router.post("/tax-planning")
async def get_tax_planning_advice(income: float, current_deductions: dict):
    """Get tax planning advice"""
    try:
        if income <= 0:
            raise HTTPException(status_code=400, detail="Income must be greater than 0")
        
        # Generate tax planning advice
        advice = await gemini_service.generate_tax_planning_advice(
            income=income,
            current_deductions=current_deductions
        )
        
        return {
            "advice": advice,
            "income": income,
            "current_deductions": current_deductions,
            "generated_at": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating tax planning advice: {str(e)}")
        raise HTTPException(status_code=500, detail="Error generating tax planning advice")


@router.post("/document-analysis")
async def analyze_document(document_content: str, document_type: str):
    """Analyze a financial document"""
    try:
        if not document_content.strip():
            raise HTTPException(status_code=400, detail="Document content cannot be empty")
        
        # Generate document analysis
        analysis = await gemini_service.analyze_financial_document(
            document_content=document_content,
            document_type=document_type
        )
        
        return {
            "analysis": analysis,
            "document_type": document_type,
            "content_length": len(document_content),
            "analyzed_at": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing document: {str(e)}")
        raise HTTPException(status_code=500, detail="Error analyzing document")


async def get_document_content(document_id: str) -> Optional[str]:
    """Helper function to get document content"""
    try:
        # This would typically query a document store
        # For now, return None as this is handled by the document service
        return None
    except Exception as e:
        logger.error(f"Error getting document content: {str(e)}")
        return None


def generate_suggestions(query_type: str) -> List[str]:
    """Generate follow-up suggestions based on query type"""
    suggestions = {
        "savings": [
            "How much should I save for emergency fund?",
            "What are the best savings account options?",
            "How to create a monthly budget?"
        ],
        "investment": [
            "What are good mutual funds for beginners?",
            "Should I invest in stocks or mutual funds?",
            "How to start SIP investment?"
        ],
        "tax": [
            "What are the best tax-saving investments?",
            "How to maximize Section 80C deductions?",
            "What documents do I need for tax filing?"
        ],
        "loan": [
            "How to calculate EMI for different loan amounts?",
            "What is the best home loan interest rate?",
            "How to improve credit score?"
        ],
        "general": [
            "Tell me about personal finance basics",
            "What are the current RBI interest rates?",
            "How to plan for retirement?"
        ]
    }
    
    return suggestions.get(query_type, suggestions["general"])
