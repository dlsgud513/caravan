
class ReservationException(Exception):
    """예약 관련 에러의 기본 클래스"""
    pass

class UserNotFoundException(ReservationException):
    """사용자를 찾을 수 없을 때 발생하는 예외"""
    def __init__(self, user_id: int):
        self.user_id = user_id
        super().__init__(f"User with ID '{self.user_id}' not found.")

class CaravanNotFoundException(ReservationException):
    """카라반을 찾을 수 없을 때 발생하는 예외"""
    def __init__(self, caravan_id: int):
        self.caravan_id = caravan_id
        super().__init__(f"Caravan with ID '{self.caravan_id}' not found.")

class CaravanNotAvailableException(ReservationException):
    """카라반이 특정 날짜에 이용 불가능할 때 발생하는 예외"""
    def __init__(self, caravan_id: int, start_date, end_date):
        self.caravan_id = caravan_id
        self.start_date = start_date
        self.end_date = end_date
        super().__init__(
            f"Caravan with ID '{self.caravan_id}' is not available "
            f"between {self.start_date} and {self.end_date}."
        )

class InsufficientFundsException(ReservationException):
    """사용자 잔액이 부족할 때 발생하는 예외"""
    def __init__(self, user_id: int, required_amount: float, balance: float):
        self.user_id = user_id
        self.required_amount = required_amount
        self.balance = balance
        super().__init__(
            f"User with ID '{self.user_id}' has insufficient funds. "
            f"Required: {self.required_amount}, Available: {self.balance}."
        )

class InvalidReservationDatesException(ReservationException):
    """예약 날짜가 유효하지 않을 때 발생하는 예외"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)
