from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ChatMessage(BaseModel):
    role: MessageRole
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    context: Optional[Dict[str, Any]] = None
    document_ids: Optional[List[str]] = None


class ChatResponse(BaseModel):
    message: str
    sources: Optional[List[Dict[str, Any]]] = None
    suggestions: Optional[List[str]] = None
    timestamp: datetime = Field(default_factory=datetime.now)


class ChatHistory(BaseModel):
    messages: List[ChatMessage]
    session_id: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class ChatSession(BaseModel):
    session_id: str
    title: str
    message_count: int
    created_at: datetime
    updated_at: datetime
