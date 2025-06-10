try:
    from . import chatbot_pb2
    from . import chatbot_pb2_grpc

    __all__ = ['chatbot_pb2', 'chatbot_pb2_grpc']
except ImportError:
    # protobuf가 아직 컴파일되지 않은 경우
    __all__ = []
