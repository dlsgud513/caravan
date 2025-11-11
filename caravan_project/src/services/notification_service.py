
from typing import Dict, Set

class NotificationService:
    """
    사용자 알림을 관리하고 전송을 시뮬레이션하는 서비스.
    실제 환경에서는 WebSocket 연결 관리자 또는 메시지 큐와 연동됩니다.
    """
    def __init__(self):
        # 현재 '온라인' 상태인 사용자 ID를 저장하는 집합
        self._online_users: Set[int] = set()

    def connect(self, user_id: int):
        """사용자가 연결(온라인)되었음을 시뮬레이션합니다."""
        print(f"[System] 사용자 {user_id}가 연결되었습니다.")
        self._online_users.add(user_id)

    def disconnect(self, user_id: int):
        """사용자 연결이 끊어졌음(오프라인)을 시뮬레이션합니다."""
        print(f"[System] 사용자 {user_id}가 연결 해제되었습니다.")
        self._online_users.discard(user_id)

    def send(self, user_id: int, message: str):
        """특정 사용자에게 알림을 보냅니다."""
        if user_id in self._online_users:
            # 사용자가 온라인일 경우, 실시간 메시지 전송을 시뮬레이션
            print(f"   L [WebSocket] 사용자(ID: {user_id})에게 전송: \"{message}\"")
        else:
            # 사용자가 오프라인일 경우, 나중에 전송하기 위해 큐에 저장함을 시뮬레이션
            print(f"  L [Offline] 사용자(ID: {user_id})의 알림을 큐에 저장: \"{message}\"")


