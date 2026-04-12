import random
from typing import Tuple, Optional

class YooMoneyMockGateway:
    FAILURE_REASONS = [
        "insufficient_funds",
        "card_expired",
        "bank_declined",
        "gateway_timeout"
    ]

    @staticmethod
    def process_payment(user_id: str, amount: float) -> Tuple[bool, Optional[str]]:
        # Симуляция обработки: 70% успех, 30% отказ
        if random.random() < 0.7:
            return True, None
        return False, random.choice(YooMoneyMockGateway.FAILURE_REASONS)