
# 1. 도메인 모델 정의 (Data Models)
# 각 객체의 속성을 명확히 정의합니다.
class User:
    def __init__(self, id, name, balance=0):
        self.id = id
        self.name = name
        self.balance = balance

class Caravan:
    def __init__(self, id, name, owner_id):
        self.id = id
        self.name = name
        self.owner_id = owner_id

class Reservation:
    def __init__(self, id, user_id, caravan_id, start_date, end_date, price, status='pending'):
        self.id = id
        self.user_id = user_id
        self.caravan_id = caravan_id
        self.start_date = start_date
        self.end_date = end_date
        self.price = price
        self.status = status

# 2. 저장소 클래스 정의 (Repositories)
# 데이터 컬렉션을 관리하고 효율적인 검색을 제공합니다.
class BaseRepository:
    """딕셔너리를 사용해 O(1) 시간 복잡도로 데이터를 검색합니다."""
    def __init__(self):
        self._data = {}
        self._next_id = 1

    def find_by_id(self, id):
        return self._data.get(id)

    def save(self, entity):
        if not hasattr(entity, 'id') or entity.id is None:
            entity.id = self._next_id
            self._next_id += 1
        self._data[entity.id] = entity
        return entity

class UserRepository(BaseRepository): pass
class CaravanRepository(BaseRepository): pass

class ReservationRepository(BaseRepository):
    """예약 관련 비즈니스 로직에 특화된 검색 기능을 추가합니다."""
    def is_caravan_reserved(self, caravan_id, start_date, end_date):
        for reservation in self._data.values():
            if reservation.caravan_id == caravan_id:
                # 날짜 겹치는지 확인
                if (start_date < reservation.end_date and end_date > reservation.start_date):
                    return True
        return False

# 3. 서비스 클래스 정의 (Services)
# 비즈니스 로직을 캡슐화하고, 다른 컴포넌트와 협력합니다.
class PaymentService:
    """결제 로직을 독립적으로 분리하여 다른 시스템으로 교체하기 쉽게 만듭니다."""
    def process_payment(self, user, price):
        if user.balance < price:
            print(f"결제 실패: 잔액 부족 (사용자: {user.name}, 잔액: {user.balance}, 필요 금액: {price})")
            return False
        user.balance -= price
        print(f"결제 성공: {price}원 (사용자: {user.name}, 남은 잔액: {user.balance})")
        return True

class ReservationService:
    """
    의존성 주입(DI)을 통해 필요한 저장소와 서비스를 외부에서 받습니다.
    이를 통해 테스트 시 Mock 객체를 주입하기 용이해집니다.
    """
    def __init__(self, user_repo, caravan_repo, reservation_repo, payment_service):
        self.user_repo = user_repo
        self.caravan_repo = caravan_repo
        self.reservation_repo = reservation_repo
        self.payment_service = payment_service

    def create_reservation(self, user_id, caravan_id, start_date, end_date, price):
        # 1. 데이터 조회 (각 저장소에 위임)
        user = self.user_repo.find_by_id(user_id)
        caravan = self.caravan_repo.find_by_id(caravan_id)

        if not user or not caravan:
            print("예약 실패: 사용자 또는 카라반 정보를 찾을 수 없습니다.")
            return None

        # 2. 예약 가능 여부 검사 (저장소에 위임)
        if self.reservation_repo.is_caravan_reserved(caravan_id, start_date, end_date):
            print("예약 실패: 해당 날짜에 이미 예약된 카라반입니다.")
            return None

        # 3. 결제 처리 (결제 서비스에 위임)
        if not self.payment_service.process_payment(user, price):
            return None
            
        # 4. 예약 생성 및 저장
        new_reservation = Reservation(None, user_id, caravan_id, start_date, end_date, price)
        self.reservation_repo.save(new_reservation)
        
        print(f"예약 성공: {user.name}님이 {caravan.name}을(를) 예약했습니다.")
        return new_reservation

# --- 실행 예시 ---
if __name__ == "__main__":
    # 1. 의존성 설정 (객체 생성)
    user_repo = UserRepository()
    caravan_repo = CaravanRepository()
    reservation_repo = ReservationRepository()
    payment_service = PaymentService()
    
    reservation_service = ReservationService(
        user_repo, caravan_repo, reservation_repo, payment_service
    )

    # 2. 초기 데이터 생성
    user1 = user_repo.save(User(id=None, name="김민준", balance=1000))
    user2 = user_repo.save(User(id=None, name="이서연", balance=500))
    
    caravan1 = caravan_repo.save(Caravan(id=None, name="모던 카라반", owner_id=user2.id))

    # 3. 서비스 실행
    print("--- 첫 번째 예약 시도 ---")
    reservation_service.create_reservation(user1.id, caravan1.id, "2025-12-20", "2025-12-23", 300)
    
    print("\n--- 중복된 날짜에 두 번째 예약 시도 ---")
    reservation_service.create_reservation(user2.id, caravan1.id, "2025-12-22", "2025-12-25", 400)
    
    print("\n--- 잔액 부족한 사용자의 세 번째 예약 시도 ---")
    reservation_service.create_reservation(user2.id, caravan1.id, "2025-12-26", "2025-12-28", 600)

    print("\n--- 네 번째 예약 시도 ---")
    reservation_service.create_reservation(user1.id, caravan1.id, "2025-12-29", "2025-12-31", 200)

