import logging
import threading
import uuid
from datetime import datetime, timedelta
from typing import Dict, Optional, List

from langchain_core.language_models import BaseChatModel

from .agent import Agent, AgentException
from .concepts import CHARACTERS


class SessionManager:
    """Agent 세션을 관리하는 클래스"""

    def __init__(self, llm: BaseChatModel, session_timeout_minutes: int = 60):
        self.llm = llm
        self.sessions: Dict[str, Agent] = {}
        self.session_timestamps: Dict[str, datetime] = {}
        self.session_timeout = timedelta(minutes=session_timeout_minutes)
        self._lock = threading.RLock()

        # 세션 정리를 위한 타이머 설정
        self._cleanup_timer = None
        self._start_cleanup_timer()

    def _start_cleanup_timer(self):
        """주기적으로 만료된 세션을 정리하는 타이머 시작"""
        def cleanup():
            self._cleanup_expired_sessions()
            self._start_cleanup_timer()  # 다음 정리 스케줄링

        if self._cleanup_timer:
            self._cleanup_timer.cancel()

        # 10분마다 정리 수행
        self._cleanup_timer = threading.Timer(600.0, cleanup)
        self._cleanup_timer.daemon = True
        self._cleanup_timer.start()

    def _cleanup_expired_sessions(self):
        """만료된 세션들을 정리"""
        with self._lock:
            current_time = datetime.now()
            expired_sessions = []

            for session_id, timestamp in self.session_timestamps.items():
                if current_time - timestamp > self.session_timeout:
                    expired_sessions.append(session_id)

            for session_id in expired_sessions:
                self._remove_session(session_id)
                logging.info(f"Expired session removed: {session_id}")

    def _remove_session(self, session_id: str):
        """세션 제거 (내부 메서드)"""
        self.sessions.pop(session_id, None)
        self.session_timestamps.pop(session_id, None)

    def _update_session_timestamp(self, session_id: str):
        """세션의 마지막 활동 시간 업데이트"""
        self.session_timestamps[session_id] = datetime.now()

    def create_session(
            self,
            session_id: Optional[str] = None,
            character_role: str = "바르곤",
            opponent_role: str = "나크티스",
            language: str = "korean"
    ) -> str:
        """새로운 세션 생성"""
        with self._lock:
            # 세션 ID 생성 또는 검증
            if session_id is None:
                session_id = str(uuid.uuid4())
            elif session_id in self.sessions:
                raise AgentException(f"Session {session_id} already exists")

            # 캐릭터 검증
            if character_role not in CHARACTERS:
                raise AgentException(f"Unknown character: {character_role}")
            if opponent_role not in CHARACTERS:
                raise AgentException(f"Unknown opponent: {opponent_role}")

            try:
                # Agent 인스턴스 생성
                concept = CHARACTERS[character_role]
                opponent_concept = CHARACTERS[opponent_role]

                agent = Agent(
                    llm=self.llm,
                    concept=concept,
                    language=language,
                    opponent_concept=opponent_concept
                )

                # 세션 등록
                self.sessions[session_id] = agent
                self._update_session_timestamp(session_id)

                logging.info(f"Session created: {session_id}, Character: {character_role}, Opponent: {opponent_role}")
                return session_id

            except Exception as e:
                logging.error(f"Failed to create session: {e}")
                raise AgentException(f"Failed to create session: {e}")

    def get_session(self, session_id: str) -> Agent:
        """세션의 Agent 인스턴스 반환"""
        with self._lock:
            if session_id not in self.sessions:
                raise AgentException(f"Session {session_id} not found")

            self._update_session_timestamp(session_id)
            return self.sessions[session_id]

    def remove_session(self, session_id: str) -> bool:
        """세션 제거"""
        with self._lock:
            if session_id in self.sessions:
                self._remove_session(session_id)
                logging.info(f"Session removed: {session_id}")
                return True
            return False

    def list_sessions(self) -> List[str]:
        """활성 세션 목록 반환"""
        with self._lock:
            return list(self.sessions.keys())

    def session_exists(self, session_id: str) -> bool:
        """세션 존재 여부 확인"""
        with self._lock:
            return session_id in self.sessions

    def get_session_info(self, session_id: str) -> Dict:
        """세션 정보 반환"""
        with self._lock:
            if session_id not in self.sessions:
                raise AgentException(f"Session {session_id} not found")

            agent = self.sessions[session_id]
            timestamp = self.session_timestamps[session_id]

            return {
                "session_id": session_id,
                "character_role": agent.concept.role,
                "opponent_role": agent.opponent_concept.role,
                "language": agent.language,
                "created_at": timestamp.isoformat(),
                "last_activity": timestamp.isoformat()
            }

    def get_all_sessions_info(self) -> List[Dict]:
        """모든 세션 정보 반환"""
        with self._lock:
            return [self.get_session_info(session_id) for session_id in self.sessions.keys()]

    def shutdown(self):
        """세션 매니저 종료"""
        with self._lock:
            if self._cleanup_timer:
                self._cleanup_timer.cancel()
            self.sessions.clear()
            self.session_timestamps.clear()
            logging.info("SessionManager shutdown completed")

    def __len__(self) -> int:
        """활성 세션 수 반환"""
        with self._lock:
            return len(self.sessions)