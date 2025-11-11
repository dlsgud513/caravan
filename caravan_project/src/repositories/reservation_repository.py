
from collections import defaultdict
from datetime import date
from typing import Dict, List, Optional

from caravan_project.models.reservation import Reservation
from .base_repository import BaseRepository

class ReservationRepository(BaseRepository[Reservation]):
    """
    예약 데이터에 특화된 저장소.
    카라반 ID별로 예약을 그룹화하여 날짜 충돌 검사 성능을 최적화합니다.
    """
    def __init__(self):
        super().__init__()
        # caravan_id를 키로 사용하여 예약을 그룹화하는 인덱스
        self._reservations_by_caravan: Dict[int, List[Reservation]] = defaultdict(list)

    def save(self, reservation: Reservation) -> Reservation:
        """예약을 저장하고 카라반 ID 기반 인덱스에도 추가합니다."""
        super().save(reservation)
        self._reservations_by_caravan[reservation.caravan_id].append(reservation)
        return reservation

    def find_by_caravan_id(self, caravan_id: int) -> List[Reservation]:
        """특정 카라반의 모든 예약을 조회합니다."""
        return self._reservations_by_caravan.get(caravan_id, [])

    def check_caravan_availability(self, caravan_id: int, start_date: date, end_date: date) -> bool:
        """
        최적화된 방식으로 특정 카라반이 주어진 날짜에 이용 가능한지 확인합니다.
        해당 카라반의 예약 목록만 순회하므로 전체 예약을 순회하는 것보다 훨씬 효율적입니다.
        """
        reservations_for_caravan = self.find_by_caravan_id(caravan_id)
        
        for reservation in reservations_for_caravan:
            # 예약 상태가 'confirmed'인 경우에만 충돌 검사
            if reservation.status == 'confirmed':
                # 기존 예약과 날짜가 겹치는지 확인
                # (start1 < end2) and (start2 < end1)
                if start_date < reservation.end_date and end_date > reservation.start_date:
                    return False # 겹치는 예약이 있으므로 이용 불가능
        
        return True # 겹치는 예약이 없으므로 이용 가능
