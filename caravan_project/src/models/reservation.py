
from dataclasses import dataclass
from datetime import date

# 과제 4: 상수 네이밍 가이드 적용
MIN_RESERVATION_DAYS = 1

@dataclass
class Reservation:
    """예약 정보를 관리하는 데이터 클래스"""
    reservation_id: int
    user_id: int
    caravan_id: int
    start_date: date
    end_date: date
    total_price: float
    status: str = 'pending' # e.g., pending, confirmed, cancelled

    def __post_init__(self):
        """객체 생성 후 데이터 유효성을 검사합니다."""
        if self.start_date >= self.end_date:
            raise ValueError("Start date must be before end date.")
        if (self.end_date - self.start_date).days < MIN_RESERVATION_DAYS:
            raise ValueError(f"Reservation must be for at least {MIN_RESERVATION_DAYS} day(s).")

