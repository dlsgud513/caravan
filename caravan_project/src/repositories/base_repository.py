
from typing import TypeVar, Generic, Dict, Optional

T = TypeVar('T')

class BaseRepository(Generic[T]):
    """
    제네릭 저장소 클래스.
    딕셔너리를 사용하여 ID 기반으로 데이터를 효율적으로 관리 (O(1) 시간 복잡도).
    """
    def __init__(self):
        self._data: Dict[int, T] = {}
        self._next_id: int = 1

    def find_by_id(self, entity_id: int) -> Optional[T]:
        """ID로 엔티티를 검색합니다."""
        return self._data.get(entity_id)

    def save(self, entity: T) -> T:
        """엔티티를 저장합니다. ID가 없으면 새로 할당합니다."""
        entity_id = getattr(entity, 'id', None) or getattr(entity, f"{type(entity).__name__.lower()}_id")

        if entity_id is None:
            entity_id = self._next_id
            setattr(entity, f"{type(entity).__name__.lower()}_id", entity_id)
            self._next_id += 1
        
        self._data[entity_id] = entity
        return entity

    def get_all(self) -> list[T]:
        """모든 엔티티를 리스트로 반환합니다."""
        return list(self._data.values())
