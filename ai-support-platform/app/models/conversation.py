from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class Conversation(BaseModel):
    id: Optional[str] = Field(None, alias="_id")

    ticket_id: str

    # Who is involved
    customer_id: str
    agent_id: str                 # AI agent identifier

    # Lifecycle
    started_at: datetime = Field(default_factory=datetime.utcnow)
    ended_at: Optional[datetime] = None

    # State
    status: str = "active"        # active | paused | ended | escalated

    # Risk & AI annotations (populated later)
    risk_flags: List[str] = []
