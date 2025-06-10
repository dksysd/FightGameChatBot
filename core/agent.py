import json
import uuid
from typing import Literal, Optional
import logging

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import MessagesState, END
from langgraph.graph.state import CompiledStateGraph, StateGraph
from pydantic import BaseModel, Field, ValidationError

from models.concept import Concept
from models.response import Response


class Process(BaseModel):
    action: Literal["chat", "analysis", "done"] = Field(description="사용자가 원하는 동작")
    query: str = Field(description="사용자 질의")


class ProcessState(MessagesState):
    process: Optional[Process] = None
    initialized: bool = False  # 초기화 상태 추가


class AgentException(Exception):
    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return self.message


class Agent:
    def __init__(self, llm: BaseChatModel, concept: Concept, language: str, opponent_concept: Concept):
        self.__llm: BaseChatModel = llm
        self.__language: str = language
        self.__concept: Concept = concept
        self.__opponent_concept: Concept = opponent_concept
        self.__config: RunnableConfig = {"configurable": {"thread_id": str(uuid.uuid4())}}
        self.__chat_prompt_message: SystemMessage = self.__generate_chat_prompt_message(
            language=language, opponent_concept=opponent_concept
        )
        self.__memory: MemorySaver = MemorySaver()
        self.__graph: CompiledStateGraph = self.__build_graph()

        # 로깅 설정
        logging.getLogger("langchain_google_genai.chat_models").setLevel(logging.ERROR)

        # 에이전트 초기화 - 그래프 실행하여 초기화 완료
        self._initialize_agent()

    def _initialize_agent(self):
        """에이전트 초기화 - init만 실행하고 멈춤"""
        try:
            # 초기화만 실행하는 상태
            initial_state = ProcessState(
                messages=[],
                process=Process(action="done", query="init"),  # done으로 설정해서 초기화 후 바로 종료
                initialized=False
            )
            result = self.__graph.invoke(input=initial_state, config=self.__config)
            logging.info("Agent initialized successfully")
        except Exception as e:
            logging.error(f"Agent initialization failed: {e}")
            raise AgentException(f"Failed to initialize agent: {e}")

    @staticmethod
    def __generate_chat_prompt_message(language: str, opponent_concept: Concept) -> SystemMessage:
        chat_output_parser: PydanticOutputParser = PydanticOutputParser(pydantic_object=Response)
        chat_prompt = PromptTemplate(
            template="Must answer in {language}. Wrap the output in `json` tags.\n{format_instruction}",
            input_variables=["language", "opponent_character"],
            partial_variables={"format_instruction": chat_output_parser.get_format_instructions()}
        )
        return SystemMessage(
            chat_prompt.invoke(input={"language": language, "opponent_character": opponent_concept.role}).to_string()
        )

    def __build_graph(self) -> CompiledStateGraph:
        def init_agent_node(state: ProcessState) -> ProcessState:
            # 이미 초기화된 경우 스킵
            if state.get("initialized", False):
                return state

            # 캐릭터 소개
            query = f"모든 대답은 다음 언어로 답하라. {self.__language}. 너는 {self.__concept.role}이다. 상대방과 너는 같은 존재일 수 있다. \n캐릭터 정보:{self.__concept.model_dump_json()}"
            state["messages"].append(SystemMessage(content=query))
            response = self.__llm.invoke(input=SystemMessage(content=query).model_dump_json(), config=self.__config)
            state["messages"].append(AIMessage(content=response.content))

            # 상대방 소개
            opponent_intro = f"나는 {self.__opponent_concept.role}, {self.__opponent_concept.group}다."
            state["messages"].append(HumanMessage(content=opponent_intro))
            response = self.__llm.invoke(input=state["messages"], config=self.__config)
            state["messages"].append(AIMessage(content=response.content))

            # 초기화 완료 표시
            state["initialized"] = True
            return state

        def process_input_node(state: ProcessState) -> ProcessState:
            # process가 미리 설정되어 있어야 함
            process = state.get("process")
            if not process:
                raise AgentException("No process found in state")

            if process.action == "chat":
                chat_content = {
                    "speech": process.query,
                    "role": self.__opponent_concept.role,
                    "group": self.__opponent_concept.group
                }
                state["messages"].append(HumanMessage(content=json.dumps(chat_content)))

            elif process.action == "analysis":
                analysis_content = {
                    "query": "상대방의 행동에 따른 상황을 분석하여 적절한 대답과 감정을 도출하라.",
                    "opponent_actions": process.query
                }
                state["messages"].append(SystemMessage(content=json.dumps(analysis_content)))

            return state

        def generate_chat_response_node(state: ProcessState) -> ProcessState:
            try:
                # 채팅 프롬프트 추가
                state["messages"].append(self.__chat_prompt_message)

                structured_llm = self.__llm.with_structured_output(schema=Response)
                response = structured_llm.invoke(input=state["messages"], config=self.__config)

                response_content = {
                    "speech": response.speech,
                    "emotion": response.emotion
                }
                state["messages"].append(AIMessage(content=json.dumps(response_content)))
                return state
            except Exception as e:
                logging.error(f"Chat response generation failed: {e}")
                error_response = {
                    "speech": "죄송합니다. 응답을 생성할 수 없습니다.",
                    "emotion": "당황"
                }
                state["messages"].append(AIMessage(content=json.dumps(error_response)))
                return state

        def analysis_game_state_node(state: ProcessState) -> ProcessState:
            try:
                response = self.__llm.invoke(input=state["messages"], config=self.__config)
                state["messages"].append(AIMessage(content=response.content))
                return state
            except Exception as e:
                logging.error(f"Game state analysis failed: {e}")
                state["messages"].append(AIMessage(content="분석을 수행할 수 없습니다."))
                return state

        def route_process(state: ProcessState) -> Literal["chat", "analysis", "done"]:
            process = state.get("process")
            if not process:
                return "done"
            return process.action

        def check_initialization(state: ProcessState) -> Literal["init", "process"]:
            """초기화 여부에 따라 라우팅"""
            if not state.get("initialized", False):
                return "init"
            return "process"

        # 그래프 구성
        builder = StateGraph(ProcessState)
        builder.add_node("check_init", lambda state: state)  # 더미 노드
        builder.add_node("init_agent", init_agent_node)
        builder.add_node("process_input", process_input_node)
        builder.add_node("generate_chat_response", generate_chat_response_node)
        builder.add_node("analysis_game_state", analysis_game_state_node)

        builder.set_entry_point("check_init")

        # 조건부 라우팅으로 초기화 확인
        builder.add_conditional_edges("check_init", check_initialization, {
            "init": "init_agent",
            "process": "process_input"
        })

        builder.add_edge("init_agent", END)  # 초기화 후 바로 종료

        builder.add_conditional_edges("process_input", route_process, {
            "chat": "generate_chat_response",
            "analysis": "analysis_game_state",
            "done": END
        })
        builder.add_edge("generate_chat_response", END)
        builder.add_edge("analysis_game_state", END)

        return builder.compile(checkpointer=self.__memory)

    def chat(self, user_message: str) -> Response:
        """채팅 메시지 처리"""
        try:
            # 현재 상태 가져오기
            current_state = self.__get_current_state()

            # Process 설정하여 상태 생성
            process = Process(action="chat", query=user_message)
            state = ProcessState(
                process=process,
                messages=current_state.get("messages", []),
                initialized=current_state.get("initialized", True)  # 이미 초기화됨
            )

            result = self.__graph.invoke(input=state, config=self.__config)

            # 마지막 메시지에서 응답 추출
            if result["messages"]:
                last_message = result["messages"][-1]
                if isinstance(last_message, AIMessage):
                    try:
                        response_data = json.loads(last_message.content)
                        return Response(
                            speech=response_data.get("speech", "응답을 생성할 수 없습니다."),
                            emotion=response_data.get("emotion", "당황")
                        )
                    except json.JSONDecodeError:
                        return Response(speech=last_message.content, emotion="보통")

            # 기본 응답
            return Response(speech="응답을 생성할 수 없습니다.", emotion="당황")

        except Exception as e:
            logging.error(f"Chat processing failed: {e}")
            return Response(speech="오류가 발생했습니다.", emotion="당황")

    def analyze_game_state(self, opponent_actions: str) -> str:
        """게임 상태 분석"""
        try:
            # 현재 상태 가져오기
            current_state = self.__get_current_state()

            # Process 설정하여 상태 생성
            process = Process(action="analysis", query=opponent_actions)
            state = ProcessState(
                process=process,
                messages=current_state.get("messages", []),
                initialized=current_state.get("initialized", True)  # 이미 초기화됨
            )

            result = self.__graph.invoke(input=state, config=self.__config)

            # 마지막 메시지에서 분석 결과 추출
            if result["messages"]:
                last_message = result["messages"][-1]
                if isinstance(last_message, AIMessage):
                    return last_message.content

            return "분석을 수행할 수 없습니다."

        except Exception as e:
            logging.error(f"Game state analysis failed: {e}")
            return "분석 중 오류가 발생했습니다."

    def __get_current_state(self) -> dict:
        """현재 대화 상태 가져오기"""
        try:
            # 메모리에서 현재 상태 조회
            snapshot = self.__memory.get(self.__config)
            if snapshot:
                return snapshot
            else:
                return {"messages": [], "initialized": True}
        except Exception as e:
            logging.warning(f"Failed to get current state: {e}")
            return {"messages": [], "initialized": True}

    def reset_conversation(self):
        """대화 기록 초기화"""
        try:
            # 새로운 thread_id 생성
            self.__config = {"configurable": {"thread_id": str(uuid.uuid4())}}
            # 에이전트 재초기화
            self._initialize_agent()
            logging.info("Conversation reset successfully")
        except Exception as e:
            logging.error(f"Failed to reset conversation: {e}")
            raise AgentException(f"Failed to reset conversation: {e}")

    def get_conversation_history(self) -> list:
        """대화 기록 조회"""
        try:
            current_state = self.__get_current_state()
            return current_state.get("messages", [])
        except Exception as e:
            logging.warning(f"Failed to get conversation history: {e}")
            return []

    def display_mermaid_image(self):
        """Mermaid 다이어그램 표시 (개발용)"""
        try:
            import io
            from PIL import Image
            img_bytes = io.BytesIO(self.__graph.get_graph().draw_mermaid_png())
            Image.open(img_bytes).show()
        except ImportError:
            print("PIL이 설치되지 않아 다이어그램을 표시할 수 없습니다.")
        except Exception as e:
            print(f"다이어그램 표시 실패: {e}")

    @property
    def concept(self) -> Concept:
        """현재 캐릭터 컨셉 반환"""
        return self.__concept

    @property
    def opponent_concept(self) -> Concept:
        """상대방 캐릭터 컨셉 반환"""
        return self.__opponent_concept

    @property
    def language(self) -> str:
        """현재 언어 설정 반환"""
        return self.__language