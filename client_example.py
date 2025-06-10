"""
gRPC 클라이언트 예제

실제 환경에서는 protobuf 컴파일 후 사용:
python -m grpc_tools.protoc --python_out=./generated --grpc_python_out=./generated --proto_path=./proto chatbot.proto
"""

import asyncio
import logging

# 실제 환경에서 사용할 import
import grpc
from generated import chatbot_pb2, chatbot_pb2_grpc


class MockGRPCClient:
    """Mock gRPC 클라이언트 (protobuf 없이 테스트용)"""

    def __init__(self, server_address: str = "localhost:50051"):
        self.server_address = server_address
        self.logger = logging.getLogger(__name__)

    async def connect(self):
        """서버 연결"""
        # 실제 환경에서는:
        self.channel = grpc.aio.insecure_channel(self.server_address)
        self.stub = chatbot_pb2_grpc.CharacterChatServiceStub(self.channel)
        self.logger.info(f"Connecting to {self.server_address}")

    async def disconnect(self):
        """연결 해제"""
        # 실제 환경에서는:
        if hasattr(self, 'channel'):
            await self.channel.close()
        self.logger.info("Disconnected from server")

    async def init_session(self, character_role: str, opponent_role: str, language: str = "korean", session_id: str = None):
        """세션 초기화"""
        # 실제 환경에서는:
        request = chatbot_pb2.InitSessionRequest(
            session_id=session_id or "",
            character_role=character_role,
            opponent_role=opponent_role,
            language=language
        )
        response = await self.stub.InitSession(request)
        return response

        # self.logger.info(f"세션 초기화: {character_role} vs {opponent_role} ({language})")
        # return {
        #     "success": True,
        #     "session_id": "mock-session-id",
        #     "error_message": ""
        # }

    async def chat(self, session_id: str, message: str):
        """채팅 메시지 전송"""
        # 실제 환경에서는:
        request = chatbot_pb2.ChatRequest(
            session_id=session_id,
            user_message=message
        )
        response = await self.stub.Chat(request)
        return response

        # self.logger.info(f"채팅 전송: {message}")
        # return {
        #     "speech": "안녕하세요! 저는 바르곤입니다.",
        #     "emotion": "자신감",
        #     "success": True,
        #     "error_message": ""
        # }

    async def analyze_game_state(self, session_id: str, opponent_actions: str):
        """게임 상태 분석"""
        # 실제 환경에서는:
        request = chatbot_pb2.AnalysisRequest(
            session_id=session_id,
            opponent_actions=opponent_actions
        )
        response = await self.stub.AnalyzeGameState(request)
        return response

        # self.logger.info(f"게임 상태 분석: {opponent_actions}")
        # return {
        #     "analysis": "상대방이 공격적인 자세를 취하고 있어 방어적인 전략이 필요합니다.",
        #     "success": True,
        #     "error_message": ""
        # }

    async def end_session(self, session_id: str):
        """세션 종료"""
        # 실제 환경에서는:
        request = chatbot_pb2.EndSessionRequest(session_id=session_id)
        response = await self.stub.EndSession(request)
        return response

        # self.logger.info(f"세션 종료: {session_id}")
        # return {
        #     "success": True,
        #     "error_message": ""
        # }

    async def list_sessions(self):
        """활성 세션 목록 조회"""
        # 실제 환경에서는:
        request = chatbot_pb2.ListSessionsRequest()
        response = await self.stub.ListSessions(request)
        return response

        # self.logger.info("세션 목록 조회")
        # return {
        #     "session_ids": ["mock-session-id", "another-session-id"]
        # }

    async def stream_chat(self, session_id: str, messages: list):
        """스트림 채팅"""
        # 실제 환경에서는:
        async def request_generator():
            for message in messages:
                yield chatbot_pb2.ChatRequest(
                    session_id=session_id,
                    user_message=message
                )

        responses = []
        async for response in self.stub.StreamChat(request_generator()):
            responses.append(response)
        return responses

        # self.logger.info(f"스트림 채팅: {len(messages)}개 메시지")
        # responses = []
        # for i, message in enumerate(messages):
        #     responses.append({
        #         "speech": f"응답 {i+1}: {message}에 대한 답변입니다.",
        #         "emotion": "호기심",
        #         "success": True,
        #         "error_message": ""
        #     })
        # return responses


async def run_client_example():
    """클라이언트 예제 실행"""
    logging.basicConfig(level=logging.INFO)

    client = MockGRPCClient()

    try:
        # 1. 서버 연결
        await client.connect()

        # 2. 세션 초기화
        init_response = await client.init_session(
            character_role="바르곤",
            opponent_role="카게츠",
            language="korean"
        )
        print(f"세션 초기화 응답: {init_response}")

        if init_response.success:
            session_id = init_response.session_id

            # 3. 채팅 테스트
            chat_response = await client.chat(session_id, "안녕하세요! 오늘 날씨가 좋네요.")
            print(f"채팅 응답: {chat_response}")

            # 4. 게임 상태 분석 테스트
            analysis_response = await client.analyze_game_state(
                session_id,
                "상대방이 공격적인 자세를 취하며 다가오고 있습니다."
            )
            print(f"분석 응답: {analysis_response}")

            # 5. 세션 목록 조회
            list_response = await client.list_sessions()
            print(f"세션 목록: {list_response}")

            # 6. 스트림 채팅 테스트
            stream_messages = ["첫 번째 메시지", "두 번째 메시지", "세 번째 메시지"]
            stream_responses = await client.stream_chat(session_id, stream_messages)
            print(f"스트림 응답: {stream_responses}")

            # 7. 세션 종료
            end_response = await client.end_session(session_id)
            print(f"세션 종료 응답: {end_response}")

    except Exception as e:
        print(f"클라이언트 오류: {e}")

    finally:
        await client.disconnect()


# 실제 gRPC 클라이언트 (protobuf 사용)
class RealGRPCClient:
    """실제 gRPC 클라이언트 구현"""

    def __init__(self, server_address: str = "localhost:50051"):
        self.server_address = server_address
        self.channel = None
        self.stub = None

    async def connect(self):
        """서버 연결"""
        self.channel = grpc.aio.insecure_channel(self.server_address)
        self.stub = chatbot_pb2_grpc.CharacterChatServiceStub(self.channel)
        # pass

    async def disconnect(self):
        """연결 해제"""
        if self.channel:
            await self.channel.close()
        # pass

    # 나머지 메서드들도 실제 protobuf 메시지를 사용하여 구현


if __name__ == "__main__":
    asyncio.run(run_client_example())