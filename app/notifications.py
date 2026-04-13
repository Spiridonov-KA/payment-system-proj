from datetime import datetime
from app.config import NOTIFICATION_FILE

def send_notification(payment_id: int, status: str, reason: str = None):
    timestamp = datetime.utcnow().isoformat()
    message = f"[{timestamp}] Payment #{payment_id} | Status: {status}"
    if reason:
        message += f" | Reason: {reason}"
    message += "\n"
    with open(NOTIFICATION_FILE, "a", encoding="utf-8") as f:
        f.write(message)