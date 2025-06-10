import os
import dotenv


class Config:
    """설정 관리 클래스"""

    def __init__(self):
        dotenv.load_dotenv()
        self.model = os.getenv('MODEL', 'gemini-pro')
        self.temperature = float(os.getenv('TEMPERATURE', "0.7"))
        self.top_p = float(os.getenv('TOP_P', "0.95"))
        self.grpc_port = int(os.getenv('GRPC_PORT', "50051"))
        self.max_workers = int(os.getenv('MAX_WORKERS', "10"))
        self.session_timeout_minutes = int(os.getenv('SESSION_TIMEOUT_MINUTES', "60"))
        self.log_level = os.getenv('LOG_LEVEL', 'INFO')

    def validate(self):
        """설정 검증"""
        if not os.getenv('GOOGLE_API_KEY'):
            raise ValueError("GOOGLE_API_KEY environment variable is required")

        if self.temperature < 0 or self.temperature > 2:
            raise ValueError("TEMPERATURE must be between 0 and 2")

        if self.top_p < 0 or self.top_p > 1:
            raise ValueError("TOP_P must be between 0 and 1")

        if self.grpc_port < 1024 or self.grpc_port > 65535:
            raise ValueError("GRPC_PORT must be between 1024 and 65535")

    def __str__(self):
        return f"""Configuration:
        Model: {self.model}
        Temperature: {self.temperature}
        Top P: {self.top_p}
        gRPC Port: {self.grpc_port}
        Max Workers: {self.max_workers}
        Session Timeout: {self.session_timeout_minutes} minutes
        Log Level: {self.log_level}
        """
