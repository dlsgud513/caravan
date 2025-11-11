
from dataclasses import dataclass

@dataclass
class Review:
    """리뷰 및 평가 정보를 관리하는 데이터 클래스"""
    review_id: int
    user_id: int
    caravan_id: int
    rating: int # 1-5
    comment: str

    def __post_init__(self):
        """객체 생성 후 데이터 유효성을 검사합니다."""
        if not 1 <= self.rating <= 5:
            raise ValueError("Rating must be between 1 and 5.")
