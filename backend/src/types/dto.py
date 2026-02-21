"""
Data Transfer Objects (DTOs)
"""

from pydantic import BaseModel
from src.types.cases import CaseDSAProblem, CaseSoftwareDesignProblem


class InterviewStartResponse(BaseModel):
    system_prompt: str
    cases: list[CaseDSAProblem | CaseSoftwareDesignProblem]


class TavusUtteranceResponse(BaseModel):
    response: str
    feedback: list[str] | None = None
    possible_follow_ups: list[str] | None = None
    clarity_score: float | None = None
    correctness: str
