from pydantic import BaseModel, Field


# noinspection SpellCheckingInspection
class Response(BaseModel):
    """사용자의 말에 대한 캐릭터의 반응"""
    speech: str = Field(description="캐릭터가 생성하는 대사")
    emotion: str = Field(description="캐릭터가 느끼는 감정")
