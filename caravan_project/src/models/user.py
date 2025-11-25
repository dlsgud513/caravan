from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    """사용자 정보를 관리하는 Pydantic 모델"""
    user_id: Optional[int] = None
    email: str
    name: str
    hashed_password: Optional[str] = None # For direct authentication
    picture: Optional[str] = None
    balance: float = 0.0
    provider: Optional[str] = None # e.g., 'google', 'kakao'
    social_id: Optional[str] = None # Provider-specific user ID

    def has_sufficient_balance(self, amount: float) -> bool:
        """사용자가 특정 금액을 지불할 충분한 잔액을 가지고 있는지 확인합니다."""
        return self.balance >= amount

    def deduct_balance(self, amount: float):
        """사용자 잔액에서 금액을 차감합니다."""
        if not self.has_sufficient_balance(amount):
            raise ValueError("Insufficient balance")
        self.balance -= amount