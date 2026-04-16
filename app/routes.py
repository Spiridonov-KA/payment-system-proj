from datetime import datetime, timedelta, timezone
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi import Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Payment, PaymentStatus
from app.schemas import PaymentCreate, PaymentResponse
from app.gateway import YooMoneyMockGateway
from app.config import settings
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
        db_payment.next_retry_at = datetime.now(timezone.utc) + timedelta(hours=settings.RETRY_DELAY_HOURS)
        send_notification(db_payment.id, "FAILED", failure_reason)

    db.commit()
    db.refresh(db_payment)
    return db_payment

@router.get("/", response_model=List[PaymentResponse])
def list_payments(
    skip: int = Query(default=0, ge=0, description="Пропустить N записей"),
    limit: int = Query(default=50, ge=1, le=100, description="Максимум записей"),
    status: PaymentStatus | None = Query(None, description="Фильтр по статусу"),
    db: Session = Depends(get_db)
):
    stmt = select(Payment)
    if status:
        stmt = stmt.where(Payment.status == status)
    stmt = stmt.order_by(Payment.created_at.desc()).offset(skip).limit(limit)
    return db.execute(stmt).scalars().all()

@router.get("/{payment_id}", response_model=PaymentResponse)
def get_payment(payment_id: int, db: Session = Depends(get_db)):
    stmt = select(Payment).where(Payment.id == payment_id)
    payment = db.execute(stmt).scalars().first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment

@router.post("/{payment_id}/refund", response_model=PaymentResponse)
def refund_payment(payment_id: int, db: Session = Depends(get_db)):
    stmt = select(Payment).where(Payment.id == payment_id)
    payment = db.execute(stmt).scalars().first()
    
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    
    if payment.status != PaymentStatus.SUCCESS:
        raise HTTPException(
            status_code=400, 
            detail=f"Cannot refund payment with status: {payment.status}"
        )
    
    success, failure_reason = YooMoneyMockGateway.process_payment(payment.user_id, payment.amount)
    
    if success:
        payment.status = PaymentStatus.REFUNDED
        send_notification(payment.id, "REFUNDED")
    else:
        payment.failure_reason = f"Refund failed: {failure_reason}"
        send_notification(payment.id, "REFUND_FAILED", failure_reason)
        
    db.commit()
    db.refresh(payment)
    return payment