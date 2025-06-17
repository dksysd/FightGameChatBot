#!/usr/bin/env python3
"""
gRPC 서버 Health Check 스크립트
"""
import asyncio
import sys
import grpc
from generated import chatbot_pb2, chatbot_pb2_grpc


async def check_health():
    """gRPC 서버 Health Check"""
    try:
        # gRPC 채널 생성
        async with grpc.aio.insecure_channel('localhost:50051') as channel:
            # Health 서비스 스텁 생성
            stub = chatbot_pb2_grpc.HealthStub(channel)
            
            # Health Check 요청
            request = chatbot_pb2.HealthCheckRequest(service="chatbot.CharacterChatService")
            
            # 타임아웃 설정 (5초)
            response = await stub.Check(request, timeout=5.0)
            
            if response.status == chatbot_pb2.HealthCheckResponse.SERVING:
                print("Health check: SERVING")
                return 0
            else:
                print(f"Health check: {response.status}")
                return 1
                
    except Exception as e:
        print(f"Health check failed: {e}")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(check_health())
    sys.exit(exit_code)