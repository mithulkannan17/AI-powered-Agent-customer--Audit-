from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class Ticket(BaseModel):
    id: Optional[str] = Field(None, alias="_id")

    # Core ownership
    customer_id: str
    order_id: Optional[str] = None
    product_id: Optional[str] = None

    # Issue definition
    category: str                 # delivery, refund, product_info, etc.
    subject: str                  # short human-readable title
    description: Optional[str] = None

    # State machine (IMPORTANT)
    status: str = "open"           # open | provisionally_resolved | closed | escalated

    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Outcome tracking (used later by ML)
    resolved_at: Optional[datetime] = None
    closed_reason: Optional[str] = None

    # Risk flags (populated by AI later)
    risk_flags: List[str] = []

    # IRR
    irr_label: Optional[int] = None             # 1 = resolved, 0 = unresolved
    irr_confidence: Optional[float] = None      # model / rule confidence
    outcome_determined_at: Optional[datetime] = None

