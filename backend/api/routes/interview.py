from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class Message(BaseModel):
    role: str  # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    messages: list[Message]


@router.post("/interview/chat")
def interview_chat(request: ChatRequest):
    from agents.interviewer import run_interview

    response = run_interview([{"role": m.role, "content": m.content} for m in request.messages])
    return {"message": response}
