# gRPC 캐릭터 채팅봇 서비스

LangGraph 프레임워크를 사용하여 구현된 캐릭터 기반 채팅봇을 gRPC 서비스로 변환한 프로젝트입니다.

## 📋 목차

- [기능 개요](#기능-개요)
- [프로젝트 구조](#프로젝트-구조)
- [설치 및 설정](#설치-및-설정)
- [사용 방법](#사용-방법)
- [API 문서](#api-문서)
- [개발 가이드](#개발-가이드)

## 🎯 기능 개요

### 주요 기능
- **다중 세션 관리**: 여러 클라이언트의 동시 접속 지원
- **캐릭터별 AI 에이전트**: 바르곤(외계인), 나크티스(하피), 카게츠(닌자) 캐릭터
- **실시간 채팅**: gRPC 스트림을 통한 실시간 대화
- **게임 상태 분석**: 상황에 따른 전략적 분석 제공
- **세션 생명주기 관리**: 자동 세션 정리 및 타임아웃 처리

### 지원 캐릭터
- **바르곤**: 지구 침략을 위해 온 외계인 군 간부
- **나크티스**: 인체 실험으로 탄생한 하피 (독수리+인간)
- **카게츠**: 외계인에 맞서는 닌자 가문의 후예

## 📁 프로젝트 구조

```
grpc_chatbot/
├── proto/
│   └── chatbot.proto                    # gRPC 서비스 정의
├── generated/                           # protobuf 컴파일 결과
│   ├── chatbot_pb2.py
│   └── chatbot_pb2_grpc.py
├── models/                              # 데이터 모델
│   ├── concept.py                       # 캐릭터 컨셉 모델
│   ├── response.py                      # 응답 모델
│   └── speech_example.py                # 대사 예시 모델
├── core/                                # 핵심 로직
│   ├── agent.py                         # 수정된 Agent 클래스
│   ├── concepts.py                      # 캐릭터 정의
│   └── session_manager.py               # 세션 관리
├── services/                            # gRPC 서비스
│   └── character_chat_service.py        # 서비스 구현
├── utils/
│   └── config.py                        # 설정 관리
├── server.py                            # 서버 실행 스크립트
├── client_example.py                    # 테스트 클라이언트
├── requirements.txt                     # 의존성 목록
├── .env.example                         # 환경 변수 예시
└── README.md
```

## 🚀 설치 및 설정

### 1. 환경 준비

```bash
# Python 3.8+ 필요
python --version

# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 또는
venv\Scripts\activate     # Windows
```

### Docker로 실행하기

프로젝트를 Docker 컨테이너로 배포하고 실행할 수 있습니다.

#### 1. Docker 이미지 빌드

```bash
# 스크립트 사용
chmod +x scripts/docker-build.sh
./scripts/docker-build.sh

# 또는 직접 명령어 사용
docker build -t grpc-chatbot:latest .
```

#### 2. Docker 컨테이너 실행

```bash
# 스크립트 사용
chmod +x scripts/docker-run.sh
./scripts/docker-run.sh

# 또는 직접 명령어 사용
docker run -d --name grpc-chatbot-service -p 50051:50051 --env-file .env grpc-chatbot:latest
```

#### 3. Docker Compose 사용하기

```bash
# .env 파일이 필요합니다
docker-compose up -d
```

### 2. 의존성 설치

```bash
pip install -r requirements.txt
```

### 3. protobuf 컴파일

```bash
# generated 폴더 생성
mkdir -p generated

# protobuf 컴파일
python -m grpc_tools.protoc \
    --python_out=./generated \
    --grpc_python_out=./generated \
    --proto_path=./proto \
    chatbot.proto
```

### 4. 환경 변수 설정

```bash
# .env 파일 생성
cp .env.example .env

# Google API Key 설정 (필수)
# GOOGLE_API_KEY=your_actual_api_key_here
```

## 🎮 사용 방법

### 서버 실행

```bash
# 실제 gRPC 서버 실행
python server.py

# 테스트 모드 실행 (protobuf 없이)
python server.py test
```

### 클라이언트 테스트

```bash
# 예제 클라이언트 실행
python client_example.py
```

### 기본 사용 흐름

1. **세션 초기화**
   ```python
   # 바르곤 캐릭터로 세션 시작
   response = await client.init_session(
       character_role="바르곤",
       opponent_role="카게츠", 
       language="korean"
   )
   session_id = response.session_id
   ```

2. **채팅 대화**
   ```python
   # 사용자 메시지 전송
   response = await client.chat(session_id, "안녕하세요!")
   print(f"캐릭터 응답: {response.speech}")
   print(f"감정: {response.emotion}")
   ```

3. **게임 상태 분석**
   ```python
   # 상황 분석 요청
   response = await client.analyze_game_state(
       session_id, 
       "상대방이 공격적으로 다가오고 있습니다."
   )
   print(f"분석 결과: {response.analysis}")
   ```

4. **세션 종료**
   ```python
   await client.end_session(session_id)
   ```

## 📖 API 문서

### gRPC 서비스 메서드

#### InitSession
세션을 초기화하고 캐릭터를 설정합니다.

```protobuf
rpc InitSession(InitSessionRequest) returns (InitSessionResponse);
```

#### Chat
캐릭터와 대화를 나눕니다.

```protobuf
rpc Chat(ChatRequest) returns (ChatResponse);
```

#### AnalyzeGameState
게임 상황을 분석합니다.

```protobuf
rpc AnalyzeGameState(AnalysisRequest) returns (AnalysisResponse);
```

#### StreamChat
실시간 스트림 채팅을 지원합니다.

```protobuf
rpc StreamChat(stream ChatRequest) returns (stream ChatResponse);
```

### 메시지 타입

자세한 메시지 타입은 `proto/chatbot.proto` 파일을 참조하세요.

## 🛠 개발 가이드

### 새로운 캐릭터 추가

1. `core/concepts.py`에 새 캐릭터 정의:
   ```python
   NewCharacter: Concept = Concept(
       role="새캐릭터",
       group="소속집단",
       backstory="배경이야기",
       personality="성격",
       speech_examples=[...]
   )
   ```

2. `CHARACTERS` 딕셔너리에 추가:
   ```python
   CHARACTERS = {
       "바르곤": Vargon,
       "나크티스": Naktis,
       "카게츠": Kagetsu,
       "새캐릭터": NewCharacter,
   }
   ```

### 커스텀 LLM 사용

`server.py`에서 LLM 설정을 변경할 수 있습니다:

```python
# Ollama 사용 예시
from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="gemma3:1b-it-qat",
    temperature=config.temperature,
    top_p=config.top_p,
    base_url="http://localhost:11434"
)
```

### 로깅 설정

환경 변수 `LOG_LEVEL`로 로깅 레벨을 조정할 수 있습니다:
- DEBUG: 상세한 디버그 정보
- INFO: 일반적인 정보 (기본값)
- WARNING: 경고 메시지만
- ERROR: 오류 메시지만

### 성능 튜닝

1. **Worker 수 조정**: `MAX_WORKERS` 환경 변수
2. **세션 타임아웃**: `SESSION_TIMEOUT_MINUTES` 환경 변수
3. **LLM 파라미터**: `TEMPERATURE`, `TOP_P` 환경 변수

## 🔧 개발 도구

### 테스트 실행

```bash
# 기본 기능 테스트
python server.py test

# 단위 테스트 (pytest 설치 후)
pytest tests/
```

### 코드 포맷팅

```bash
# black 사용
pip install black
black .

# isort 사용
pip install isort
isort .
```

## 📝 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다.

## 🤝 기여하기

1. 이 저장소를 포크합니다
2. 새 기능 브랜치를 생성합니다 (`git checkout -b feature/새기능`)
3. 변경사항을 커밋합니다 (`git commit -am '새 기능 추가'`)
4. 브랜치를 푸시합니다 (`git push origin feature/새기능`)
5. Pull Request를 생성합니다

## 🆘 문제해결

### 자주 발생하는 문제

1. **GOOGLE_API_KEY 오류**
    - `.env` 파일에 올바른 API 키가 설정되었는지 확인
    - Google AI Studio에서 API 키 발급 필요

2. **protobuf 컴파일 오류**
    - `grpcio-tools` 패키지가 설치되었는지 확인
    - `generated` 폴더가 존재하는지 확인

3. **세션 시간 초과**
    - `SESSION_TIMEOUT_MINUTES` 환경 변수로 타임아웃 조정
    - 세션 활동이 없으면 자동으로 정리됨

4. **메모리 사용량 증가**
    - 주기적으로 만료된 세션이 정리됨
    - `MAX_WORKERS` 수를 줄여 메모리 사용량 조절

### 지원

문제가 발생하면 GitHub Issues에 보고해주세요.