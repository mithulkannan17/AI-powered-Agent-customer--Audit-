from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Product(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    name: str
    description: str
    price: float
    created_at: datetime = Field(default_factory=datetime.utcnow)
