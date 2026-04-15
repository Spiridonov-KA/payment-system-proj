from datetime import datetime, timezone
from app.config import settings

def send_notification(payment_id: int, status: str, reason: str = None):
    timestamp = datetime.now(timezone.utc).isoformat()
    message = f"[{timestamp}] Payment #{payment_id} | Status: {status}"
    if reason:
        message += f" | Reason: {reason}"
    message += "\n"
    with open(settings.NOTIFICATION_FILE, "a", encoding="utf-8") as f:
        f.write(message)