
import unittest
from unittest.mock import Mock
from datetime import date, timedelta

# Test Target
from caravan_project.validators.reservation_validator import ReservationValidator

# Models and Exceptions for testing
from caravan_project.models.user import User
from caravan_project.exceptions.custom_exceptions import (
    UserNotFoundException,
    CaravanNotFoundException,
    CaravanNotAvailableException,
    InsufficientFundsException,
    InvalidReservationDatesException,
)

class TestReservationValidator(unittest.TestCase):
    """ReservationValidator에 대한 단위 테스트"""

    def setUp(self):
        """각 테스트 전에 Mock 객체와 Validator를 초기화합니다."""
        self.user_repo = Mock()
        self.caravan_repo = Mock()
        self.reservation_repo = Mock()
        
        self.validator = ReservationValidator(
            self.user_repo, self.caravan_repo, self.reservation_repo
        )
        
        # 테스트에 사용할 기본 데이터
        self.test_user = User(user_id=1, name="Test User", balance=500.0)
        self.today = date.today()
        self.start_date = self.today + timedelta(days=1)
        self.end_date = self.today + timedelta(days=5)

    def test_validate_user_existence_success(self):
        """사용자 존재 검증 성공 케이스"""
        self.user_repo.find_by_id.return_value = self.test_user
        # 예외가 발생하지 않으면 성공
        user = self.validator._validate_user_existence(1)
        self.assertEqual(user, self.test_user)
        self.user_repo.find_by_id.assert_called_once_with(1)

    def test_validate_user_existence_raises_exception(self):
        """사용자를 찾을 수 없을 때 예외 발생 케이스"""
        self.user_repo.find_by_id.return_value = None
        with self.assertRaises(UserNotFoundException):
            self.validator._validate_user_existence(99)

    def test_validate_caravan_availability_success(self):
        """카라반 이용 가능 검증 성공 케이스"""
        self.reservation_repo.check_caravan_availability.return_value = True
        # 예외가 발생하지 않으면 성공
        self.validator._validate_caravan_availability(1, self.start_date, self.end_date)
        self.reservation_repo.check_caravan_availability.assert_called_once_with(1, self.start_date, self.end_date)

    def test_validate_caravan_availability_raises_exception(self):
        """카라반 이용 불가능 시 예외 발생 케이스"""
        self.reservation_repo.check_caravan_availability.return_value = False
        with self.assertRaises(CaravanNotAvailableException):
            self.validator._validate_caravan_availability(1, self.start_date, self.end_date)

    def test_validate_dates_success(self):
        """날짜 유효성 검증 성공 케이스"""
        # 예외가 발생하지 않으면 성공
        self.validator._validate_dates(self.start_date, self.end_date)

    def test_validate_dates_raises_exception_for_past_date(self):
        """과거 날짜 예약 시 예외 발생 케이스"""
        past_date = self.today - timedelta(days=1)
        with self.assertRaises(InvalidReservationDatesException):
            self.validator._validate_dates(past_date, self.end_date)

    def test_validate_dates_raises_exception_for_invalid_range(self):
        """종료일이 시작일보다 빠를 때 예외 발생 케이스"""
        with self.assertRaises(InvalidReservationDatesException):
            self.validator._validate_dates(self.end_date, self.start_date)

    def test_validate_user_funds_success(self):
        """사용자 잔액 충분 검증 성공 케이스"""
        # 예외가 발생하지 않으면 성공
        self.validator._validate_user_funds(self.test_user, 300.0)

    def test_validate_user_funds_raises_exception(self):
        """사용자 잔액 부족 시 예외 발생 케이스"""
        with self.assertRaises(InsufficientFundsException):
            self.validator._validate_user_funds(self.test_user, 600.0)

    def test_full_validate_success(self):
        """전체 검증 로직 성공 케이스"""
        # 모든 검증이 통과하도록 Mock 설정
        self.user_repo.find_by_id.return_value = self.test_user
        self.caravan_repo.find_by_id.return_value = Mock() # Caravan Mock
        self.reservation_repo.check_caravan_availability.return_value = True
        
        # 예외가 발생하지 않으면 성공
        self.validator.validate(1, 1, self.start_date, self.end_date, 300.0)


if __name__ == '__main__':
    unittest.main()
