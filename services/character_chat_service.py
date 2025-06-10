import asyncio
import logging
from typing import AsyncIterator

import grpc
from grpc import aio

# Generated protobuf imports - 실제 환경에서는 protobuf 컴파일 후 사용
from generated import chatbot_pb2, chatbot_pb2_grpc

from core.session_manager import SessionManager
from core.agent import AgentException


class CharacterChatService:
    """gRPC CharacterChatService 구현"""

    def __init__(self, session_manager: SessionManager):
        self.session_manager = session_manager

    async def InitSession(self, request, context):
        """세션 초기화"""
        try:
            session_id = self.session_manager.create_session(
                session_id=request.session_id if request.session_id else None,
                character_role=request.character_role,
                opponent_role=request.opponent_role,
                language=request.language
            )

            return chatbot_pb2.InitSessionResponse(
                success=True,
                session_id=session_id,
                error_message=""
            )

            # # protobuf 없이 테스트용 반환
            # return {
            #     "success": True,
            #     "session_id": session_id,
            #     "error_message": ""
            # }

        except AgentException as e:
            logging.error(f"Session initialization failed: {e}")
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(str(e))

            return chatbot_pb2.InitSessionResponse(
                success=False,
                session_id="",
                error_message=str(e)
            )

            # return {
            #     "success": False,
            #     "session_id": "",
            #     "error_message": str(e)
            # }

        except Exception as e:
            logging.error(f"Unexpected error in InitSession: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal server error")

            return {
                "success": False,
                "session_id": "",
                "error_message": "Internal server error"
            }

    async def Chat(self, request, context):
        """채팅 대화"""
        try:
            agent = self.session_manager.get_session(request.session_id)
            response = agent.chat(request.user_message)

            return chatbot_pb2.ChatResponse(
                speech=response.speech,
                emotion=response.emotion,
                success=True,
                error_message=""
            )

            # return {
            #     "speech": response.speech,
            #     "emotion": response.emotion,
            #     "success": True,
            #     "error_message": ""
            # }

        except AgentException as e:
            logging.error(f"Chat failed: {e}")
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(str(e))

            return {
                "speech": "",
                "emotion": "",
                "success": False,
                "error_message": str(e)
            }

        except Exception as e:
            logging.error(f"Unexpected error in Chat: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal server error")

            return {
                "speech": "",
                "emotion": "",
                "success": False,
                "error_message": "Internal server error"
            }

    async def AnalyzeGameState(self, request, context):
        """게임 상태 분석"""
        try:
            agent = self.session_manager.get_session(request.session_id)
            analysis = agent.analyze_game_state(request.opponent_actions)

            return chatbot_pb2.AnalysisResponse(
                analysis=analysis,
                success=True,
                error_message=""
            )

            # return {
            #     "analysis": analysis,
            #     "success": True,
            #     "error_message": ""
            # }

        except AgentException as e:
            logging.error(f"Game state analysis failed: {e}")
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(str(e))

            return {
                "analysis": "",
                "success": False,
                "error_message": str(e)
            }

        except Exception as e:
            logging.error(f"Unexpected error in AnalyzeGameState: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal server error")

            return {
                "analysis": "",
                "success": False,
                "error_message": "Internal server error"
            }

    async def EndSession(self, request, context):
        """세션 종료"""
        try:
            success = self.session_manager.remove_session(request.session_id)

            if not success:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details(f"Session {request.session_id} not found")

                return {
                    "success": False,
                    "error_message": f"Session {request.session_id} not found"
                }

            return chatbot_pb2.EndSessionResponse(
                success=True,
                error_message=""
            )

            # return {
            #     "success": True,
            #     "error_message": ""
            # }

        except Exception as e:
            logging.error(f"Unexpected error in EndSession: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal server error")

            return {
                "success": False,
                "error_message": "Internal server error"
            }

    async def ListSessions(self, request, context):
        """활성 세션 목록 조회"""
        try:
            session_ids = self.session_manager.list_sessions()

            return chatbot_pb2.ListSessionsResponse(
                session_ids=session_ids
            )

            # return {
            #     "session_ids": session_ids
            # }

        except Exception as e:
            logging.error(f"Unexpected error in ListSessions: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal server error")

            return {
                "session_ids": []
            }

    async def StreamChat(self, request_iterator, context):
        """스트림 채팅 (실시간)"""
        try:
            async for request in request_iterator:
                try:
                    agent = self.session_manager.get_session(request.session_id)
                    response = agent.chat(request.user_message)

                    yield chatbot_pb2.ChatResponse(
                        speech=response.speech,
                        emotion=response.emotion,
                        success=True,
                        error_message=""
                    )

                    # yield {
                    #     "speech": response.speech,
                    #     "emotion": response.emotion,
                    #     "success": True,
                    #     "error_message": ""
                    # }

                except AgentException as e:
                    logging.error(f"Stream chat failed: {e}")

                    yield {
                        "speech": "",
                        "emotion": "",
                        "success": False,
                        "error_message": str(e)
                    }

                except Exception as e:
                    logging.error(f"Unexpected error in stream chat: {e}")

                    yield {
                        "speech": "",
                        "emotion": "",
                        "success": False,
                        "error_message": "Internal server error"
                    }

        except Exception as e:
            logging.error(f"Unexpected error in StreamChat: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal server error")


class CharacterChatServicer:
    """실제 gRPC 서비스 구현 (protobuf 사용 시)"""

    def __init__(self, session_manager: SessionManager):
        self.service = CharacterChatService(session_manager)

    # 실제 protobuf 사용 시 이 메서드들을 활성화

    async def InitSession(self, request, context):
        return await self.service.InitSession(request, context)

    async def Chat(self, request, context):
        return await self.service.Chat(request, context)

    async def AnalyzeGameState(self, request, context):
        return await self.service.AnalyzeGameState(request, context)

    async def EndSession(self, request, context):
        return await self.service.EndSession(request, context)

    async def ListSessions(self, request, context):
        return await self.service.ListSessions(request, context)

    async def StreamChat(self, request_iterator, context):
        async for response in self.service.StreamChat(request_iterator, context):
            yield response


# Mock protobuf classes for testing without compilation
class MockRequest:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class MockChatRequest(MockRequest):
    def __init__(self, session_id: str, user_message: str):
        super().__init__(session_id=session_id, user_message=user_message)


class MockInitSessionRequest(MockRequest):
    def __init__(self, session_id: str, character_role: str, opponent_role: str, language: str):
        super().__init__(
            session_id=session_id,
            character_role=character_role,
            opponent_role=opponent_role,
            language=language
        )


class MockAnalysisRequest(MockRequest):
    def __init__(self, session_id: str, opponent_actions: str):
        super().__init__(session_id=session_id, opponent_actions=opponent_actions)


class MockEndSessionRequest(MockRequest):
    def __init__(self, session_id: str):
        super().__init__(session_id=session_id)


class MockListSessionsRequest(MockRequest):
    def __init__(self):
        super().__init__()


class MockContext:
    def __init__(self):
        self.code = None
        self.details = None

    def set_code(self, code):
        self.code = code

    def set_details(self, details):
        self.details = details