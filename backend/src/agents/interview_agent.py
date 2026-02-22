from pydantic import BaseModel, Field
from typing import List
import json
from deepagents import create_deep_agent
from src.types.dto import TavusUtteranceResponse
from src.configuration import (
    OPENAI_API_KEY,
    FIRECRAWL_API_KEY,
    LANGSMITH_API_KEY,
    LANGSMITH_ORG_ID,
)
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model

model = init_chat_model("gpt-4.1", temperature=0)


class ClarityScore(BaseModel):
    clarity_score: float = Field(ge=0, le=10)


class Feedback(BaseModel):
    feedback: List[str]


class PossibleFollowUps(BaseModel):
    possible_follow_ups: List[str]


class Correctness(BaseModel):
    correctness: str


class FinalResponse(BaseModel):
    response: str


clarity_agent = create_agent(
    model=model,
    system_prompt="""
You are evaluating the clarity of an interviewee's responses.
Return a clarity_score between 0 and 10.
Only evaluate clarity.
""",
    tools=[],
    response_format=ClarityScore,
)

feedback_agent = create_agent(
    model=model,
    system_prompt="""
Provide constructive feedback about the interviewee's performance.
Return a list of short feedback points.
""",
    tools=[],
    response_format=Feedback,
)

followups_agent = create_agent(
    model=model,
    system_prompt="""
Suggest relevant follow-up questions based on the interview.
Return a list of follow-up questions.
""",
    tools=[],
    response_format=PossibleFollowUps,
)

correctness_agent = create_agent(
    model=model,
    system_prompt="""
Evaluate whether the interviewee's responses are correct and relevant.
Return a concise evaluation paragraph.
""",
    tools=[],
    response_format=Correctness,
)

final_response_agent = create_agent(
    model=model,
    system_prompt="""
        Based on clarity score, feedback, follow-ups, and correctness,
        generate a final professional response to the interviewee.
        """,
    tools=[],
    response_format=TavusUtteranceResponse,
)


def run_agent(history: list[dict]) -> TavusUtteranceResponse:
    # ---- 1. Clarity
    clarity_result = clarity_agent.invoke({"messages": history})
    clarity_data = clarity_result["structured_response"]

    # ---- 2. Feedback
    feedback_result = feedback_agent.invoke({"messages": history})
    feedback_data = feedback_result["structured_response"]

    # ---- 3. Follow-ups
    followups_result = followups_agent.invoke({"messages": history})
    followups_data = followups_result["structured_response"]

    # ---- 4. Correctness
    correctness_result = correctness_agent.invoke({"messages": history})
    correctness_data = correctness_result["structured_response"]

    # ---- 5. Final Response
    final_result = final_response_agent.invoke(
        {
            "messages": history
            + [
                {
                    "role": "system",
                    "content": f"""
                    Clarity score: {clarity_data.clarity_score}
                    Feedback: {feedback_data.feedback}
                    Follow-ups: {followups_data.possible_follow_ups}
                    Correctness: {correctness_data.correctness}
                    """,
                }
            ]
        }
    )
    final_data = final_result["structured_response"]

    # ---- 6. Combine into Tavus DTO

    return final_data
