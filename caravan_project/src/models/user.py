
from dataclasses import dataclass, field

@dataclass
class User:
    """사용자 정보를 관리하는 데이터 클래스"""
    user_id: int
    name: str
    balance: float = 0.0
    
    def has_sufficient_balance(self, amount: float) -> bool:
        """사용자가 특정 금액을 지불할 충분한 잔액을 가지고 있는지 확인합니다."""
        return self.balance >= amount

    def deduct_balance(self, amount: float):
        """사용자 잔액에서 금액을 차감합니다."""
        if not self.has_sufficient_balance(amount):
            # 이 부분은 서비스 계층에서 예외 처리를 하는 것이 더 좋습니다.
            # 여기서는 간단한 검증만 수행합니다.
            raise ValueError("Insufficient balance")
        self.balance -= amount
