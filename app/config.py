import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'payments.db')}"
NOTIFICATION_FILE = os.path.join(BASE_DIR, "notifications.log")
RETRY_DELAY_HOURS = 24  # Повторная попытка через 1 день