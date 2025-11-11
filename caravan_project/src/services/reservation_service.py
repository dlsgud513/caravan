
from datetime import date

# Models and Repositories
from src.models.user import User
from src.models.caravan import Caravan
from src.repositories.base_repository import BaseRepository
from src.repositories.reservation_repository import ReservationRepository

# Validators and Exceptions
from src.validators.reservation_validator import ReservationValidator
from src.exceptions.custom_exceptions import ReservationException

# Design Patterns
from src.patterns.observers import Observable
from src.patterns.strategies import DiscountStrategy, NoDiscount
from src.patterns.factories import ReservationFactory


class ReservationService(Observable):
    """
    예약 생성의 전체 비즈니스 로직을 조정(Orchestrate)합니다.
    의존성 주입을 통해 모든 외부 종속성을 받으며, 테스트 가능한 구조입니다.
    Observable을 상속받아 예약 생성 시 관련 옵저버들에게 알림을 보냅니다.
    """
    def __init__(
        self,
        user_repo: BaseRepository[User],
        caravan_repo: BaseRepository[Caravan],
        reservation_repo: ReservationRepository,
        validator: ReservationValidator,
        discount_strategy: DiscountStrategy = NoDiscount()
    ):
        super().__init__()
        self.user_repo = user_repo
        self.caravan_repo = caravan_repo
        self.reservation_repo = reservation_repo
        self.validator = validator
        self.discount_strategy = discount_strategy

    def create_reservation(self, user_id: int, caravan_id: int, start_date: date, end_date: date):
        try:
            print(f"\n--- {user_id}번 사용자의 {caravan_id}번 카라반 예약 요청 ---")
            
            # 기본 가격 계산 (여기서는 간단히 일당 100으로 가정)
            base_price = 100 * (end_date - start_date).days

            # 1. 모든 비즈니스 규칙 검증 (Validator에 위임)
            self.validator.validate(user_id, caravan_id, start_date, end_date, base_price)
            print("검증 통과.")

            # 2. 할인 적용 (Strategy Pattern)
            discount = self.discount_strategy.calculate_discount(base_price, start_date, end_date)
            final_price = base_price - discount
            print(f"가격 계산: 기본 {base_price} - 할인 {discount:.2f} = 최종 {final_price:.2f}")

            # 3. 결제 처리 (User 모델의 책임)
            user = self.user_repo.find_by_id(user_id)
            user.deduct_balance(final_price)
            print(f"결제 처리 완료. (남은 잔액: {user.balance})")

            # 4. 예약 객체 생성 (Factory Pattern)
            reservation = ReservationFactory.create_reservation(
                user_id, caravan_id, start_date, end_date, final_price
            )
            print(f"예약 객체 생성 (ID: {reservation.reservation_id}, 상태: {reservation.status}).")

            # 5. 예약 정보 저장 (Repository에 위임)
            self.reservation_repo.save(reservation)
            print("예약 정보 저장 완료.")

            # 6. 옵저버들에게 알림 (Observer Pattern)
            caravan = self.caravan_repo.find_by_id(caravan_id)
            self.notify(reservation=reservation, caravan=caravan)
            
            return reservation

        except ReservationException as e:
            print(f"[예약 실패] {e}")
            return None
        except Exception as e:
            print(f"[알 수 없는 에러] {e}")
            return None
