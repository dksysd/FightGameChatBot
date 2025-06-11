# Builder Stage: Install dependencies using uv
FROM python:3.12-alpine AS builder

# Install necessary packages for building dependencies (might not always be needed, but safer)
# build-base는 크기가 크지만, 일부 패키지 컴파일에 필요할 수 있습니다.
# 만약 의존성 중에 빌드 도구가 필요하지 않다면 이 줄에서 build-base, python3-dev 등을 제거하여 빌더 이미지 크기를 줄일 수 있습니다.
RUN apk update && apk add --no-cache build-base python3-dev openssl-dev zlib-dev

# uv 설치 (빌더 이미지에만 필요)
RUN pip install uv

WORKDIR /app
COPY pyproject.toml uv.lock ./

# uv sync --frozen 명령으로 /app/.venv에 의존성 설치
RUN uv sync --frozen

# Runtime Stage: Run the application with dependencies from the builder
FROM python:3.12-alpine AS runtime

# 런타임에 필요한 패키지 설치 (wget for grpc_health_probe download, shadow for user management)
RUN apk update && apk add --no-cache shadow wget

# 사용자 홈 디렉토리의 bin에 설치
RUN mkdir -p /home/appuser/bin && \
    cd /tmp && \
    curl -L -o grpc_health_probe \
    https://github.com/grpc-ecosystem/grpc-health-probe/releases/download/v0.4.24/grpc_health_probe-linux-amd64 && \
    chmod +x grpc_health_probe && \
    mv grpc_health_probe /home/appuser/bin/ && \
    chown appuser:appuser /home/appuser/bin/grpc_health_probe

# PATH에 추가
ENV PATH="/home/appuser/bin:/app/.venv/bin:$PATH"
# 빌더에서 설치된 가상 환경 복사
COPY --from=builder /app/.venv /app/.venv

# 가상 환경의 bin 디렉토리를 PATH에 추가
# 이렇게 하면 '.venv/bin/' 안의 'python' 실행 파일과 설치된 패키지 실행 파일들을 직접 사용할 수 있습니다.
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

# PATH에 설정된 가상 환경의 python 실행 파일을 직접 사용하여 스크립트 실행
# uv 실행 파일을 런타임 이미지에 포함시키지 않아도 됩니다.
CMD ["python", "server.py"]