from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    DATABASE_URL: str = f"sqlite:///{BASE_DIR / 'payments.db'}"
    NOTIFICATION_FILE: str = "/app/logs/notifications.log"
    RETRY_DELAY_HOURS: int = 24
    SCHEDULER_INTERVAL_MINUTES: int = 1

    model_config = ConfigDict(
        env_file=str(BASE_DIR / ".env"),
        case_sensitive=False
    )

settings = Settings()