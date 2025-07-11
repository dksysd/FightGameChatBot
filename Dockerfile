# Builder Stage: Install dependencies using uv
FROM python:3.12-alpine AS builder

RUN apk update && apk add --no-cache build-base python3-dev openssl-dev zlib-dev

# uv 설치 (빌더 이미지에만 필요)
RUN pip install uv

WORKDIR /app
COPY pyproject.toml uv.lock ./

# uv sync --frozen 명령으로 /app/.venv에 의존성 설치
RUN uv sync --frozen

# Runtime Stage: Run the application with dependencies from the builder
FROM python:3.12-alpine AS runtime

# 런타임에 필요한 패키지 설치
RUN apk update && apk add --no-cache shadow curl

# grpc_health_probe를 시스템 경로에 설치 (권한 문제 없음)
RUN curl -L -o /usr/local/bin/grpc_health_probe \
    https://github.com/grpc-ecosystem/grpc-health-probe/releases/download/v0.4.24/grpc_health_probe-linux-amd64 && \
    chmod +x /usr/local/bin/grpc_health_probe && \
    grpc_health_probe --version

# 빌더에서 설치된 가상 환경 복사
COPY --from=builder /app/.venv /app/.venv

# 가상 환경의 bin 디렉토리를 PATH에 추가
ENV PATH="/app/.venv/bin:$PATH"

# 비root 사용자 생성
RUN groupadd -r appuser && useradd -r -g appuser -m appuser

WORKDIR /app
COPY . .

# 애플리케이션 코드 소유권을 비root 사용자로 변경
RUN chown -R appuser:appuser /app

# 비root 사용자로 전환
USER appuser

EXPOSE 50051

CMD ["python", "server.py"]