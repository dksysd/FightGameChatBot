from pydantic import BaseModel, Field

from .speech_example import SpeechExample

# noinspection SpellCheckingInspection
class Concept(BaseModel):
    """캐릭터의 대한 상세한 정보"""
    role: str = Field(description="캐릭터 역할")
    group: str = Field(description="캐릭터가 속해 있는 집단")
    backstory: str = Field(description="캐릭터가 지닌 배경 이야기")
    personality: str = Field(description="캐릭터의 성격")
    speech_examples: list[SpeechExample] = Field(description="상황에 따른 캐릭터의 반응 예시")