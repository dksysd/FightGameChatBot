from pydantic import BaseModel, Field


# noinspection SpellCheckingInspection
class SpeechExample(BaseModel):
    """캐릭터가 상황에 따라 대답하는 예시"""
    situation: str = Field(description="캐릭터의 상황")
    speeches: list[str] = Field(description="예상 캐릭터의 대사")
