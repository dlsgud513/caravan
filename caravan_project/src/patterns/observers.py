
from abc import ABC, abstractmethod
from typing import List
from src.services.notification_service import NotificationService

class Observer(ABC):
    """옵저버 인터페이스"""
    @abstractmethod
    def update(self, subject, **kwargs):
        pass

class Observable:
    """관찰 대상 (Subject) 클래스"""
    def __init__(self):
        self._observers: List[Observer] = []

    def attach(self, observer: Observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer):
        self._observers.remove(observer)

    def notify(self, **kwargs):
        print("옵저버들에게 알림 전송...")
        for observer in self._observers:
            observer.update(self, **kwargs)

# --- Concrete Observers ---

class UserNotifier(Observer):
    """예약한 사용자에게 알림을 보내는 옵저버"""
    def __init__(self, notification_service: NotificationService):
        self.notification_service = notification_service

    def update(self, subject, **kwargs):
        reservation = kwargs.get('reservation')
        if reservation:
            message = f"예약(ID: {reservation.reservation_id})이 성공적으로 확정되었습니다."
            # NotificationService를 통해 알림 전송
            self.notification_service.send(user_id=reservation.user_id, message=message)

class HostNotifier(Observer):
    """호스트에게 알림을 보내는 옵저버"""
    def __init__(self, notification_service: NotificationService):
        self.notification_service = notification_service

    def update(self, subject, **kwargs):
        reservation = kwargs.get('reservation')
        caravan = kwargs.get('caravan')
        if reservation and caravan:
            message = f"'{caravan.name}'에 대한 신규 예약(ID: {reservation.reservation_id})이 있습니다."
            # NotificationService를 통해 알림 전송
            self.notification_service.send(user_id=caravan.owner_id, message=message)

class StockManager(Observer):
    """재고 또는 카라반 상태를 관리하는 옵저버 (알림 서비스와 무관)"""
    def update(self, subject, **kwargs):
        caravan = kwargs.get('caravan')
        if caravan:
            print(f"   L [Stock] '{caravan.name}'(ID: {caravan.caravan_id})의 상태를 '예약됨'으로 변경합니다.")
