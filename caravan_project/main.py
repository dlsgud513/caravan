
from datetime import date, timedelta

# Models
from src.models.user import User
from src.models.caravan import Caravan
from src.models.review import Review

# Repositories
from src.repositories.base_repository import BaseRepository
from src.repositories.reservation_repository import ReservationRepository

# Services
from src.services.reservation_service import ReservationService
from src.services.notification_service import NotificationService
from src.services.review_service import ReviewService
from src.services.recommendation_service import RecommendationService
from src.validators.reservation_validator import ReservationValidator

# Patterns
from src.patterns.observers import UserNotifier, HostNotifier, StockManager
from src.patterns.strategies import LongStayDiscount

def main():
    """애플리케이션의 메인 실행 함수"""
    print("--- CaravanShare 애플리케이션 초기화 ---")

    # 1. 핵심 서비스 및 저장소 인스턴스화
    user_repo = BaseRepository[User]()
    caravan_repo = BaseRepository[Caravan]()
    reservation_repo = ReservationRepository()
    review_repo = BaseRepository[Review]()
    notification_service = NotificationService()
    recommendation_service = RecommendationService(caravan_repo) # 추천 서비스 추가
    print("저장소 및 알림/추천 서비스 준비 완료.")

    # 2. 초기 데이터 생성
    host_user = user_repo.save(User(user_id=101, name="박호스트", balance=0))
    caravan_repo.save(Caravan(caravan_id=1, name="모던 카라반", owner_id=host_user.user_id, type="Motorhome"))
    caravan_repo.save(Caravan(caravan_id=2, name="빈티지 캠퍼", owner_id=host_user.user_id, type="Campervan"))
    caravan_repo.save(Caravan(caravan_id=3, name="가족용 트레일러", owner_id=host_user.user_id, type="Motorhome"))
    caravan_repo.save(Caravan(caravan_id=4, name="오프로드 익스플로러", owner_id=202, type="Off-road"))
    print(f"테스트 데이터 생성 완료.")

    # 3. 비즈니스 로직 컴포넌트 인스턴스화 (의존성 주입)
    validator = ReservationValidator(user_repo, caravan_repo, reservation_repo)
    reservation_service = ReservationService(
        user_repo, caravan_repo, reservation_repo, validator, discount_strategy=LongStayDiscount()
    )
    review_service = ReviewService(review_repo, reservation_repo, caravan_repo)
    print("모든 서비스 및 검증기 준비 완료.")

    # 4. 옵저버(Observers) 설정 (생략)
    # ...

    # --- 시나리오 실행 ---
    
    # 시나리오 1: 사용자가 '모던 카라반' 예약
    print("\n--- 시나리오 1: 카라반 예약 ---")
    user1 = user_repo.save(User(user_id=1, name="김민준", balance=2000.0))
    target_caravan_id = 1
    start_date_1 = date.today() + timedelta(days=10)
    end_date_1 = start_date_1 + timedelta(days=5)
    reservation_service.create_reservation(user1.user_id, target_caravan_id, start_date_1, end_date_1)

    # 시나리오 2: 예약한 카라반과 유사한 카라반 추천받기
    print(f"\n--- 시나리오 2: 유사 카라반 추천 ---")
    print(f"'{caravan_repo.find_by_id(target_caravan_id).name}'(ID:{target_caravan_id})와 유사한 카라반을 추천합니다.")
    
    recommendations = recommendation_service.recommend_similar_caravans(target_caravan_id)
    
    if recommendations:
        for rec in recommendations:
            print(f"  L 추천: '{rec.name}' (ID: {rec.caravan_id}, 타입: {rec.type}, 소유주: {rec.owner_id})")
    else:
        print("  L 추천할 만한 유사 카라반이 없습니다.")


if __name__ == "__main__":
    main()
