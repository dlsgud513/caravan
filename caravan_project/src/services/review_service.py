
from src.models.review import Review
from src.models.caravan import Caravan
from src.repositories.base_repository import BaseRepository
from src.repositories.reservation_repository import ReservationRepository

class ReviewService:
    """리뷰 및 평가 관련 비즈니스 로직을 처리하는 서비스"""
    def __init__(
        self,
        review_repo: BaseRepository[Review],
        reservation_repo: ReservationRepository,
        caravan_repo: BaseRepository[Caravan]
    ):
        self.review_repo = review_repo
        self.reservation_repo = reservation_repo
        self.caravan_repo = caravan_repo

    def submit_review(self, user_id: int, caravan_id: int, rating: int, comment: str) -> Review:
        """
        사용자가 카라반에 대한 리뷰를 제출합니다.
        실제로는 사용자가 해당 카라반을 이용했는지 검증하는 로직이 필요합니다.
        """
        # 1. (검증) 사용자가 해당 카라반을 예약했었는지 확인 (여기서는 간단히 시뮬레이션)
        reservations = self.reservation_repo.get_all()
        can_review = any(
            res.user_id == user_id and res.caravan_id == caravan_id and res.status == 'confirmed'
            for res in reservations
        )
        if not can_review:
            raise PermissionError("User has not made a confirmed reservation for this caravan.")

        # 2. 리뷰 객체 생성 및 저장
        review = Review(review_id=None, user_id=user_id, caravan_id=caravan_id, rating=rating, comment=comment)
        self.review_repo.save(review)
        print(f"[Review] 사용자(ID:{user_id})가 카라반(ID:{caravan_id})에 리뷰를 남겼습니다: \"{comment}\" (별점: {rating})")

        # 3. 카라반 평균 별점 업데이트
        caravan = self.caravan_repo.find_by_id(caravan_id)
        if caravan:
            caravan.update_rating(rating)
            self.caravan_repo.save(caravan) # 변경된 caravan 정보 다시 저장
            print(f"   L [Rating] 카라반(ID:{caravan_id})의 평균 별점이 업데이트되었습니다: {caravan.average_rating:.2f} (리뷰 {caravan.review_count}개)")
        
        return review

