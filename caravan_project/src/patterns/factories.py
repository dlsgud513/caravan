
from datetime import date
from src.models.reservation import Reservation

class ReservationFactory:
    """예약 객체 생성을 담당하는 팩토리"""
    
    _next_id = 1

    @classmethod
    def create_reservation(cls, user_id: int, caravan_id: int, start_date: date, end_date: date, total_price: float) -> Reservation:
        """
        새로운 예약 객체를 생성하고 ID를 할당합니다.
        복잡한 초기화 로직이나 ID 생성 전략을 이 곳에 캡슐화할 수 있습니다.
        """
        reservation = Reservation(
            reservation_id=cls._next_id,
            user_id=user_id,
            caravan_id=caravan_id,
            start_date=start_date,
            end_date=end_date,
            total_price=total_price,
            status='confirmed'  # 팩토리에서 초기 상태를 'confirmed'로 설정
        )
        cls._next_id += 1
        return reservation
