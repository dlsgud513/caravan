
import unittest
from unittest.mock import Mock, patch
from datetime import date, timedelta

# Test Target
from caravan_project.services.reservation_service import ReservationService

# Models and Exceptions
from caravan_project.models.user import User
from caravan_project.models.caravan import Caravan
from caravan_project.models.reservation import Reservation
from caravan_project.exceptions.custom_exceptions import CaravanNotAvailableException

class TestReservationService(unittest.TestCase):
    """ReservationService에 대한 단위 테스트"""

    def setUp(self):
        """각 테스트 전에 Mock 객체와 Service를 초기화합니다."""
        self.user_repo = Mock()
        self.caravan_repo = Mock()
        self.reservation_repo = Mock()
        self.validator = Mock()
        self.discount_strategy = Mock()
        
        self.service = ReservationService(
            self.user_repo,
            self.caravan_repo,
            self.reservation_repo,
            self.validator,
            self.discount_strategy
        )
        
        # 테스트에 사용할 기본 데이터
        self.test_user = User(user_id=1, name="Test User", balance=1000.0)
        self.test_caravan = Caravan(caravan_id=1, name="Test Caravan", owner_id=101)
        self.start_date = date.today() + timedelta(days=1)
        self.end_date = self.start_date + timedelta(days=5)

        self.user_repo.find_by_id.return_value = self.test_user
        self.caravan_repo.find_by_id.return_value = self.test_caravan

    @patch('caravan_project.patterns.factories.ReservationFactory.create_reservation')
    def test_create_reservation_success(self, mock_create_reservation):
        """예약 생성 성공 시나리오 테스트"""
        # Mock 객체 설정
        self.discount_strategy.calculate_discount.return_value = 50.0 # 50 할인
        
        # 팩토리가 반환할 Mock 예약 객체
        mock_reservation = Reservation(
            reservation_id=1, user_id=1, caravan_id=1, 
            start_date=self.start_date, end_date=self.end_date, 
            total_price=450.0, status='confirmed'
        )
        mock_create_reservation.return_value = mock_reservation
        
        # 테스트할 서비스 메서드 실행
        result = self.service.create_reservation(1, 1, self.start_date, self.end_date)

        # --- 검증 ---
        # 1. Validator가 호출되었는가?
        self.validator.validate.assert_called_once()

        # 2. 할인 전략이 호출되었는가?
        self.discount_strategy.calculate_discount.assert_called_once()

        # 3. 사용자 잔액이 차감되었는가?
        self.assertEqual(self.test_user.balance, 550.0) # 1000 - (500 - 50)

        # 4. 팩토리가 올바른 인자와 함께 호출되었는가?
        base_price = 100 * (self.end_date - self.start_date).days
        final_price = base_price - 50.0
        mock_create_reservation.assert_called_once_with(1, 1, self.start_date, self.end_date, final_price)

        # 5. 예약이 저장소에 저장되었는가?
        self.reservation_repo.save.assert_called_once_with(mock_reservation)

        # 6. 결과가 예상대로인가?
        self.assertEqual(result, mock_reservation)

    def test_create_reservation_fails_on_validation(self):
        """검증 실패 시 예약이 생성되지 않는지 테스트"""
        # Validator가 예외를 발생시키도록 설정
        self.validator.validate.side_effect = CaravanNotAvailableException(1, self.start_date, self.end_date)

        # 테스트할 서비스 메서드 실행
        result = self.service.create_reservation(1, 1, self.start_date, self.end_date)

        # --- 검증 ---
        # 1. Validator가 호출되었는가?
        self.validator.validate.assert_called_once()

        # 2. 할인, 결제, 저장 등 후속 로직이 호출되지 않았는가?
        self.discount_strategy.calculate_discount.assert_not_called()
        self.reservation_repo.save.assert_not_called()
        
        # 3. 초기 잔액이 그대로인가?
        self.assertEqual(self.test_user.balance, 1000.0)

        # 4. 결과가 None인가?
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
