from datetime import datetime, timedelta, timezone
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import select

from app.database import SessionLocal
from app.models import Payment, PaymentStatus
from app.gateway import YooMoneyMockGateway
from app.notifications import send_notification
from app.config import settings

scheduler = BackgroundScheduler()

def retry_failed_payments():
    with SessionLocal() as db:
        stmt = select(Payment).where(
            Payment.status == PaymentStatus.FAILED,
            Payment.next_retry_at <= datetime.now(timezone.utc)
        )
        due_payments = db.execute(stmt).scalars().all()

        for payment in due_payments:
            success, failure_reason = YooMoneyMockGateway.process_payment(
                payment.user_id, payment.amount
            )

            if success:
                payment.status = PaymentStatus.SUCCESS
                payment.failure_reason = None
                payment.next_retry_at = None
                send_notification(payment.id, "SUCCESS")
            else:
                payment.failure_reason = failure_reason
                payment.next_retry_at = datetime.now(timezone.utc) + timedelta(hours=settings.RETRY_DELAY_HOURS)
                send_notification(payment.id, "FAILED", failure_reason)

            db.commit()

def start_scheduler():
    if not scheduler.running:
        scheduler.add_job(
            retry_failed_payments, 
            "interval", 
            minutes=settings.SCHEDULER_INTERVAL_MINUTES
        )
        scheduler.start()

def stop_scheduler():
    if scheduler.running:
        scheduler.shutdown(wait=True)