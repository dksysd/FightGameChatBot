import asyncio
import logging
import signal
import sys
from concurrent.futures import ThreadPoolExecutor

import grpc
from grpc import aio

from langchain_google_genai import ChatGoogleGenerativeAI

from core.session_manager import SessionManager
from services.character_chat_service import CharacterChatServicer
from utils.config import Config

# 실제 protobuf 사용 시 임포트
from generated import chatbot_pb2_grpc


class GRPCServer:
    """gRPC 서버 클래스"""

    def __init__(self, port: int = 50051, max_workers: int = 10):
        self.port = port
        self.max_workers = max_workers
        self.server = None
        self.session_manager = None

        # 로깅 설정
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    async def _create_llm(self):
        """LLM 인스턴스 생성"""
        config = Config()
        return ChatGoogleGenerativeAI(
            model=config.model,
            temperature=config.temperature,
            top_p=config.top_p
        )

    async def start(self):
        """서버 시작"""
        try:
            # LLM 및 세션 매니저 초기화
            llm = await self._create_llm()
            self.session_manager = SessionManager(llm=llm, session_timeout_minutes=60)

            # gRPC 서버 생성
            self.server = aio.server(ThreadPoolExecutor(max_workers=self.max_workers))

            # 서비스 등록
            service_impl = CharacterChatServicer(self.session_manager)

            # 실제 protobuf 사용 시:
            chatbot_pb2_grpc.add_CharacterChatServiceServicer_to_server(service_impl, self.server)

            # 리스닝 포트 설정
            listen_addr = f'[::]:{self.port}'
            self.server.add_insecure_port(listen_addr)

            # 서버 시작
            await self.server.start()
            self.logger.info(f"gRPC 서버가 {listen_addr}에서 시작되었습니다.")

            # 종료 시그널 핸들러 설정
            self._setup_signal_handlers()

            # 서버 대기
            await self.server.wait_for_termination()

        except Exception as e:
            self.logger.error(f"서버 시작 실패: {e}")
            raise

    async def stop(self):
        """서버 종료"""
        if self.server:
            self.logger.info("gRPC 서버를 종료합니다...")
            await self.server.stop(grace=5.0)

        if self.session_manager:
            self.session_manager.shutdown()

        self.logger.info("서버 종료 완료")

    def _setup_signal_handlers(self):
        """시그널 핸들러 설정"""
        def signal_handler(signum, frame):
            self.logger.info(f"종료 시그널 수신: {signum}")
            asyncio.create_task(self.stop())

        signal.signal(signal.SIGTERM, signal_handler)
        signal.signal(signal.SIGINT, signal_handler)


class TestGRPCServer:
    """테스트용 gRPC 서버 (protobuf 없이 동작)"""

    def __init__(self):
        self.session_manager = None
        self.service = None

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    async def start_test_mode(self):
        """테스트 모드로 서버 시작"""
        try:
            # LLM 및 세션 매니저 초기화
            config = Config()
            llm = ChatGoogleGenerativeAI(
                model=config.model,
                temperature=config.temperature,
                top_p=config.top_p
            )

            self.session_manager = SessionManager(llm=llm, session_timeout_minutes=60)

            # 서비스 초기화
            from services.character_chat_service import CharacterChatService
            self.service = CharacterChatService(self.session_manager)

            self.logger.info("테스트 서버가 시작되었습니다.")

            # 간단한 테스트 수행
            await self._run_tests()

        except Exception as e:
            self.logger.error(f"테스트 서버 시작 실패: {e}")
            raise

    async def _run_tests(self):
        """기본 기능 테스트"""
        from services.character_chat_service import (
            MockInitSessionRequest, MockChatRequest, MockAnalysisRequest,
            MockEndSessionRequest, MockListSessionsRequest, MockContext
        )

        context = MockContext()

        # 1. 세션 초기화 테스트
        self.logger.info("=== 세션 초기화 테스트 ===")
        init_request = MockInitSessionRequest(
            session_id="test-session-1",
            character_role="바르곤",
            opponent_role="카게츠",
            language="korean"
        )

        init_response = await self.service.InitSession(init_request, context)
        self.logger.info(f"초기화 응답: {init_response}")

        if init_response["success"]:
            session_id = init_response["session_id"]

            # 2. 채팅 테스트
            self.logger.info("=== 채팅 테스트 ===")
            chat_request = MockChatRequest(
                session_id=session_id,
                user_message="안녕하세요!"
            )

            chat_response = await self.service.Chat(chat_request, context)
            self.logger.info(f"채팅 응답: {chat_response}")

            # 3. 게임 상태 분석 테스트
            self.logger.info("=== 게임 상태 분석 테스트 ===")
            analysis_request = MockAnalysisRequest(
                session_id=session_id,
                opponent_actions="상대방이 공격적인 자세를 취하고 있습니다."
            )

            analysis_response = await self.service.AnalyzeGameState(analysis_request, context)
            self.logger.info(f"분석 응답: {analysis_response}")

            # 4. 세션 목록 조회 테스트
            self.logger.info("=== 세션 목록 조회 테스트 ===")
            list_request = MockListSessionsRequest()
            list_response = await self.service.ListSessions(list_request, context)
            self.logger.info(f"세션 목록: {list_response}")

            # 5. 세션 종료 테스트
            self.logger.info("=== 세션 종료 테스트 ===")
            end_request = MockEndSessionRequest(session_id=session_id)
            end_response = await self.service.EndSession(end_request, context)
            self.logger.info(f"종료 응답: {end_response}")

        self.logger.info("=== 테스트 완료 ===")

    def stop(self):
        """테스트 서버 종료"""
        if self.session_manager:
            self.session_manager.shutdown()


async def main():
    """메인 함수"""
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        # 테스트 모드
        test_server = TestGRPCServer()
        try:
            await test_server.start_test_mode()
        except KeyboardInterrupt:
            test_server.stop()
    else:
        # 실제 서버 모드
        server = GRPCServer(port=50051, max_workers=10)
        try:
            await server.start()
        except KeyboardInterrupt:
            await server.stop()


if __name__ == "__main__":
    asyncio.run(main())