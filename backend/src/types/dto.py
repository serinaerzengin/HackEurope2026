"""
Data Transfer Objects (DTOs)
"""

from pydantic import BaseModel, Field
from src.types.cases import CaseDSAProblem, CaseSoftwareDesignProblem


class InterviewStartResponse(BaseModel):
    system_prompt: str
    cases: list[CaseDSAProblem | CaseSoftwareDesignProblem]


class TavusUtteranceRequest(BaseModel):
    utterance: str
    role: str  # "user" or "replica"
    conversation_id: str
    session_id: str | None = None


class TavusUtteranceResponse(BaseModel):
    response: str
    feedback: list[str] | None = None
    possible_follow_ups: list[str] | None = None
    clarity_score: float | None = None
    correctness: str


# --- Session DTOs ---

class CreateSessionRequest(BaseModel):
    system_prompt: str
    task_description: str


class SessionResponse(BaseModel):
    session_id: str


class PauseResponse(BaseModel):
    status: str
    phase: str


class ResumeResponse(BaseModel):
    conversation_id: str
    conversation_url: str


class InterviewReport(BaseModel):
    overall_score: float = Field(ge=0, le=10)
    strengths: list[str]
    weaknesses: list[str]
    detailed_feedback: str
    communication_score: float = Field(ge=0, le=10)
    technical_score: float = Field(ge=0, le=10)
    diagram_feedback: str | None = None
