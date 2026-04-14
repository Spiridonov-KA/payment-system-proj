from datetime import datetime, timedelta
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
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

@router.get("/", response_model=List[PaymentResponse])
def list_payments(db: Session = Depends(get_db)):
    stmt = select(Payment).order_by(Payment.created_at.desc())
    return db.execute(stmt).scalars().all()

@router.get("/{payment_id}", response_model=PaymentResponse)
def get_payment(payment_id: int, db: Session = Depends(get_db)):
    stmt = select(Payment).where(Payment.id == payment_id)
    payment = db.execute(stmt).scalars().first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment