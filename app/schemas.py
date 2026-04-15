from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from app.models import PaymentStatus

class PaymentCreate(BaseModel):
    user_id: str = Field(..., min_length=3, max_length=50)
    amount: float = Field(..., gt=0.0, description="Amount must be positive")

class PaymentResponse(BaseModel):
    id: int
    user_id: str
    amount: float
    status: PaymentStatus
    failure_reason: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    next_retry_at: Optional[datetime] = None

    model_config = {"from_attributes": True}