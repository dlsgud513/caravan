
from dataclasses import dataclass, field
from typing import List

@dataclass
class Caravan:
    """카라반 정보를 관리하는 데이터 클래스"""
    caravan_id: int
    name: str
    owner_id: int
    type: str  # e.g., 'Motorhome', 'Campervan'
    is_available: bool = True
    average_rating: float = 0.0
    review_count: int = 0

    def update_rating(self, new_rating: int):
        """새로운 리뷰가 추가될 때 평균 별점과 리뷰 수를 업데이트합니다."""
        total_rating = self.average_rating * self.review_count
        self.review_count += 1
        self.average_rating = (total_rating + new_rating) / self.review_count
