from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.models import PaymentStatus

class PaymentCreate(BaseModel):
    user_id: str
    amount: float

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