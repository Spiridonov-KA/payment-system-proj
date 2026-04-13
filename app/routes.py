from datetime import datetime, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Payment, PaymentStatus
from app.schemas import PaymentCreate, PaymentResponse
from app.gateway import YooMoneyMockGateway
from app.config import RETRY_DELAY_HOURS
from app.notifications import send_notification

router = APIRouter(prefix="/payments", tags=["payments"])

@router.post("/", response_model=PaymentResponse)
def create_payment(payload: PaymentCreate, db: Session = Depends(get_db)):
    db_payment = Payment(
        user_id=payload.user_id,
        amount=payload.amount,
        status=PaymentStatus.PENDING
    )
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)

    success, failure_reason = YooMoneyMockGateway.process_payment(
        user_id=payload.user_id,
        amount=payload.amount
    )

    if success:
        db_payment.status = PaymentStatus.SUCCESS
        send_notification(db_payment.id, "SUCCESS")
    else:
        db_payment.status = PaymentStatus.FAILED
        db_payment.failure_reason = failure_reason
        db_payment.next_retry_at = datetime.utcnow() + timedelta(hours=RETRY_DELAY_HOURS)
        send_notification(db_payment.id, "FAILED", failure_reason)

    db.commit()
    db.refresh(db_payment)
    return db_payment