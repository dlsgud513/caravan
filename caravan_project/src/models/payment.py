
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Payment:
    """결제 정보를 관리하는 데이터 클래스"""
    payment_id: int
    reservation_id: int
    amount: float
    payment_method: str
    transaction_date: datetime = field(default_factory=datetime.now)
    status: str = 'completed' # e.g., completed, failed, refunded
