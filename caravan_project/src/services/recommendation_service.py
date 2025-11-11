
from typing import List
from src.models.caravan import Caravan
from src.repositories.base_repository import BaseRepository

class RecommendationService:
    """콘텐츠 기반 추천 로직을 처리하는 서비스"""
    def __init__(self, caravan_repo: BaseRepository[Caravan]):
        self.caravan_repo = caravan_repo

    def recommend_similar_caravans(self, target_caravan_id: int, top_n: int = 3) -> List[Caravan]:
        """
        특정 카라반과 유사한 다른 카라반을 추천합니다.
        - 타입이 같으면 +2점
        - 소유주가 같으면 +1점 (같은 호스트의 다른 카라반)
        """
        all_caravans = self.caravan_repo.get_all()
        target_caravan = self.caravan_repo.find_by_id(target_caravan_id)

        if not target_caravan or len(all_caravans) <= 1:
            return []

        scores = []
        for caravan in all_caravans:
            # 자기 자신은 추천에서 제외
            if caravan.caravan_id == target_caravan_id:
                continue

            score = 0
            # 1. 타입 유사도
            if caravan.type == target_caravan.type:
                score += 2
            
            # 2. 소유주 유사도
            if caravan.owner_id == target_caravan.owner_id:
                score += 1
            
            if score > 0:
                scores.append((score, caravan))

        # 점수가 높은 순으로 정렬
        scores.sort(key=lambda x: x[0], reverse=True)

        # 상위 N개의 카라반 객체만 반환
        recommended_caravans = [caravan for score, caravan in scores[:top_n]]
        
        return recommended_caravans
