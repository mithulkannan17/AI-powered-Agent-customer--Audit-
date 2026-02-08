from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import datetime

class Event(BaseModel):
    id: Optional[str] = Field(None, alias="_id")

    # Linkage
    ticket_id: str
    conversation_id: str
    message_id: Optional[str] = None

    # Event identity
    event_type: str
    severity: str = "info"   # info | warning | critical

    # Payload (flexible, ML-friendly)
    metadata: Dict = {}

    created_at: datetime = Field(default_factory=datetime.utcnow)
