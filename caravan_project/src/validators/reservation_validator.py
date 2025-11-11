
from datetime import date

from caravan_project.repositories.base_repository import BaseRepository
from caravan_project.repositories.reservation_repository import ReservationRepository
from caravan_project.models.user import User
from caravan_project.models.caravan import Caravan
from caravan_project.exceptions.custom_exceptions import (
    UserNotFoundException,
    CaravanNotFoundException,
    CaravanNotAvailableException,
    InsufficientFundsException,
    InvalidReservationDatesException,
)

class ReservationValidator:
    """
    예약 생성 전 모든 비즈니스 규칙을 검증하는 책임을 가집니다.
    각 검증은 독립적인 메서드로 분리되어 테스트가 용이합니다.
    """
    def __init__(self, user_repo: BaseRepository[User], caravan_repo: BaseRepository[Caravan], reservation_repo: ReservationRepository):
        self.user_repo = user_repo
        self.caravan_repo = caravan_repo
        self.reservation_repo = reservation_repo

    def validate(self, user_id: int, caravan_id: int, start_date: date, end_date: date, price: float):
        """모든 검증 단계를 순서대로 실행하는 메인 메서드"""
        user = self._validate_user_existence(user_id)
        self._validate_caravan_existence(caravan_id)
        self._validate_dates(start_date, end_date)
        self._validate_caravan_availability(caravan_id, start_date, end_date)
        self._validate_user_funds(user, price)

    def _validate_user_existence(self, user_id: int) -> User:
        """사용자 존재 여부를 검증합니다."""
        user = self.user_repo.find_by_id(user_id)
        if not user:
            raise UserNotFoundException(user_id)
        return user

    def _validate_caravan_existence(self, caravan_id: int) -> Caravan:
        """카라반 존재 여부를 검증합니다."""
        caravan = self.caravan_repo.find_by_id(caravan_id)
        if not caravan:
            raise CaravanNotFoundException(caravan_id)
        return caravan

    def _validate_dates(self, start_date: date, end_date: date):
        """날짜의 유효성을 검증합니다."""
        if start_date >= end_date:
            raise InvalidReservationDatesException("Start date must be before end date.")
        if start_date < date.today():
            raise InvalidReservationDatesException("Reservation cannot be made for a past date.")

    def _validate_caravan_availability(self, caravan_id: int, start_date: date, end_date: date):
        """카라반이 해당 날짜에 이용 가능한지 검증합니다."""
        if not self.reservation_repo.check_caravan_availability(caravan_id, start_date, end_date):
            raise CaravanNotAvailableException(caravan_id, start_date, end_date)

    def _validate_user_funds(self, user: User, price: float):
        """사용자의 잔액이 충분한지 검증합니다."""
        if not user.has_sufficient_balance(price):
            raise InsufficientFundsException(user.user_id, price, user.balance)
