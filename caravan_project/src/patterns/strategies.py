
from abc import ABC, abstractmethod
from datetime import date, timedelta

class DiscountStrategy(ABC):
    """할인 전략에 대한 인터페이스"""
    @abstractmethod
    def calculate_discount(self, base_price: float, start_date: date, end_date: date) -> float:
        pass

# --- Concrete Strategies ---

class NoDiscount(DiscountStrategy):
    """할인을 적용하지 않는 기본 전략"""
    def calculate_discount(self, base_price: float, start_date: date, end_date: date) -> float:
        return 0.0

class WeekendDiscount(DiscountStrategy):
    """주말(금, 토)에 10% 할인을 적용하는 전략"""
    def calculate_discount(self, base_price: float, start_date: date, end_date: date) -> float:
        total_days = (end_date - start_date).days
        if total_days == 0:
            return 0.0
            
        weekend_days = 0
        current_date = start_date
        while current_date < end_date:
            # 금요일(4), 토요일(5)
            if current_date.weekday() in [4, 5]:
                weekend_days += 1
            current_date += timedelta(days=1)
            
        # 주말 요금에만 10% 할인 적용
        daily_price = base_price / total_days
        discount = daily_price * weekend_days * 0.10
        return discount

class LongStayDiscount(DiscountStrategy):
    """7일 이상 장기 숙박 시 전체 금액의 5%를 할인하는 전략"""
    def calculate_discount(self, base_price: float, start_date: date, end_date: date) -> float:
        if (end_date - start_date).days >= 7:
            return base_price * 0.05
        return 0.0
