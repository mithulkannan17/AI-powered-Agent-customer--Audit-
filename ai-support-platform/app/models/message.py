from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import datetime

# ✅ What client sends
class MessageInput(BaseModel):
    ticket_id: str
    sender_type: str              # customer | agent | system
    sender_id: Optional[str] = None
    text: str

    confidence: Optional[float] = None
    intent: Optional[str] = None
    entities: Optional[Dict] = None
    is_correction: bool = False
    is_escalation_request: bool = False


# ✅ What we store in DB
class Message(BaseModel):
    id: Optional[str] = Field(None, alias="_id")

    conversation_id: str
    ticket_id: str
    sender_type: str
    sender_id: Optional[str] = None
    text: str

    confidence: Optional[float] = None
    intent: Optional[str] = None
    entities: Optional[Dict] = None

    is_correction: bool = False
    is_escalation_request: bool = False

    created_at: datetime = Field(default_factory=datetime.utcnow)
