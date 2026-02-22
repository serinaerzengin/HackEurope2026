from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import time

from src.api.routes.interview import router as interview_router
from src.api.routes.tavus import router as tavus_router
from src.types.dto import (
    InterviewStartResponse,
    TavusUtteranceResponse,
    TavusUtteranceRequest,
)
from src.services.interview_preperation import generate_system_prompt, recommend_case
from src.agents.interview_agent import run_agent
from src.services.miro_service import fetch_all_board_items, build_miro_description
from src.configuration import MIRO_BOARD_ID


# Simple TTL cache so you don't hit Miro API for every utterance
_miro_cache = {"ts": 0.0, "desc": ""}


def get_miro_description_cached(ttl_seconds: int = 15) -> str:
    now = time.time()
    if _miro_cache["desc"] and (now - _miro_cache["ts"] < ttl_seconds):
        return _miro_cache["desc"]

    items = fetch_all_board_items(MIRO_BOARD_ID)
    desc = build_miro_description(items)
    print(f"Fetched and built Miro description (length {len(desc)} chars)")
    print(desc)

    _miro_cache["ts"] = now
    _miro_cache["desc"] = desc
    return desc


app = FastAPI(title="HackEurope2026 API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://tavus.daily.co"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(interview_router, prefix="/api")
app.include_router(tavus_router, prefix="/api")


@app.get("/api/health")
def health():
    return {"status": "ok"}


conversation_history = {}  # In-memory store for conversation history, keyed by conversation_id


class PreparationRequest(BaseModel):
    job_description: str
    job_link: str | None = None
    task_type: str = "dsa"


@app.post("/api/interview/preparation", response_model=InterviewStartResponse)
def create_interview_preparation_tasks(req: PreparationRequest):
    # TODO: Extract company name from job description/link via LLM. Hardcoded for now.
    company_name = "Google"

    cases = recommend_case(
        company=company_name,
        job_description=req.job_description,
        task_type=req.task_type,
    )
    system_prompt = generate_system_prompt(
        company=company_name, job_description=req.job_description, cases=cases
    )

    return InterviewStartResponse(
        system_prompt=system_prompt,
        cases=cases,
    )


@app.post("/api/tavus/utterance", response_model=TavusUtteranceResponse)
def handle_tavus_utterance(req: TavusUtteranceRequest):
    if req.conversation_id not in conversation_history:
        conversation_history[req.conversation_id] = []

    history = conversation_history[req.conversation_id]

    # Save user utterance
    history.append({"role": "user", "content": req.utterance})

    # ✅ Pull Miro board context via API (cached)
    miro_description = ""
    try:
        miro_description = get_miro_description_cached(ttl_seconds=15)
        # Inject into agent context (system message is typical)
        history.append(
            {"role": "system", "content": f"Miro board context:\n{miro_description}"}
        )
    except Exception as e:
        # Don't hard-fail the interview if Miro is unavailable
        print(f"Warning: Failed to fetch Miro context: {e}")
        history.append({"role": "system", "content": f"Miro context unavailable: {e}"})

    # Run your agent
    response = run_agent(history)

    return response


if __name__ == "__main__":
    response = run_agent([])
    print(type(response))
    print(response)
