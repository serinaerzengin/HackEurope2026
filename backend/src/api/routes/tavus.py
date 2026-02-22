from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src.configuration import TAVUS_PERSONA_ID, TAVUS_REPLICA_ID
from src.services.tavus_client import create_conversation
from src.services.mock_tasks import MOCK_TASKS

router = APIRouter()


class ConversationRequest(BaseModel):
    interview_type: str
    system_prompt: str | None = None


class ConversationResponse(BaseModel):
    conversation_id: str
    conversation_url: str


@router.post("/tavus/conversation", response_model=ConversationResponse)
async def start_conversation(req: ConversationRequest):
    # If a system_prompt is provided (from preparation endpoint), use it directly
    if req.system_prompt:
        context = req.system_prompt
        greeting = (
            f"Hi! Welcome to your {req.interview_type.replace('-', ' ')} interview. "
            f"I've prepared some tasks for you. Are you ready to get started?"
        )
    else:
        # Fall back to mock task behavior
        task = MOCK_TASKS.get(req.interview_type)
        if not task:
            raise HTTPException(
                status_code=400,
                detail=f"Unknown interview type: {req.interview_type}. Must be 'coding' or 'system-design'.",
            )

        context = (
            f"Interview type: {req.interview_type}\n"
            f"Task: {task['title']}\n"
            f"Description: {task['description']}\n"
        )
        if "difficulty" in task:
            context += f"Difficulty: {task['difficulty']}\n"
        if "complexity" in task:
            context += f"Complexity: {task['complexity']}\n"

        greeting = (
            f"Hi! Welcome to your {req.interview_type.replace('-', ' ')} interview. "
            f"Today we'll be working on: {task['title']}. Are you ready to get started?"
        )

    try:
        result = await create_conversation(
            persona_id=TAVUS_PERSONA_ID,
            replica_id=TAVUS_REPLICA_ID,
            conversation_name=f"{req.interview_type}-interview",
            conversational_context=context,
            custom_greeting=greeting,
        )
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Tavus API error: {e}")

    return ConversationResponse(
        conversation_id=result["conversation_id"],
        conversation_url=result["conversation_url"],
    )
