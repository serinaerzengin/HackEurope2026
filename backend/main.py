from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import uuid

from src.api.routes.interview import router as interview_router
from src.api.routes.tavus import router as tavus_router
from src.types.dto import (
    InterviewStartResponse,
    TavusUtteranceResponse,
    TavusUtteranceRequest,
    CreateSessionRequest,
    SessionResponse,
    PauseResponse,
    ResumeResponse,
    InterviewReport,
)
from src.services.interview_preperation import generate_system_prompt, recommend_case
from src.agents.interview_agent import run_agent, generate_report
from src.services.tavus_client import create_conversation, end_conversation
from src.configuration import TAVUS_PERSONA_ID, TAVUS_REPLICA_ID


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


# --- In-memory stores ---

conversation_history = {}  # Legacy: keyed by conversation_id

sessions: dict[str, dict] = {}  # Keyed by session_id


# --- Session Endpoints ---


@app.post("/api/interview/session", response_model=SessionResponse)
def create_session(req: CreateSessionRequest):
    session_id = str(uuid.uuid4())
    sessions[session_id] = {
        "system_prompt": req.system_prompt,
        "task_description": req.task_description,
        "phase": "intro",
        "history": [],
        "conversation_ids": [],
        "diagram_analysis": None,
    }
    return SessionResponse(session_id=session_id)


@app.post("/api/interview/{session_id}/pause", response_model=PauseResponse)
async def pause_interview(session_id: str):
    session = sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    session["phase"] = "drawing"

    # End the active Tavus conversation if any
    if session["conversation_ids"]:
        last_conv_id = session["conversation_ids"][-1]
        await end_conversation(last_conv_id)

    return PauseResponse(status="paused", phase="drawing")


@app.post("/api/interview/{session_id}/resume", response_model=ResumeResponse)
async def resume_interview(session_id: str):
    session = sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # Analyze the Miro board diagram
    diagram_analysis = None
    try:
        from src.agents.diagram_agent import analyze_diagram

        analysis = await analyze_diagram()
        diagram_analysis = analysis.model_dump()
        session["diagram_analysis"] = diagram_analysis
        print(f"[resume] Diagram analysis: {diagram_analysis['summary']}")
    except Exception as e:
        print(f"[resume] Warning: diagram analysis failed: {e}")
        diagram_analysis = {
            "summary": "Could not analyze the diagram.",
            "components": [],
            "connections": [],
            "potential_issues": [],
            "probe_areas": ["Ask the candidate to describe their design verbally"],
        }
        session["diagram_analysis"] = diagram_analysis

    # Build enriched context for the new Tavus conversation
    context_parts = [
        f"Original Task:\n{session['task_description']}",
        "\nSystem Design Diagram Analysis:",
        f"Summary: {diagram_analysis['summary']}",
    ]
    if diagram_analysis.get("components"):
        context_parts.append(
            f"Components identified: {', '.join(diagram_analysis['components'])}"
        )
    if diagram_analysis.get("connections"):
        context_parts.append(
            f"Data flows: {', '.join(diagram_analysis['connections'])}"
        )
    if diagram_analysis.get("potential_issues"):
        context_parts.append(
            f"Potential issues to probe: {', '.join(diagram_analysis['potential_issues'])}"
        )
    if diagram_analysis.get("probe_areas"):
        context_parts.append(
            f"\nInterview guidance — ask about: {', '.join(diagram_analysis['probe_areas'])}"
        )

    context_parts.append(
        "\nInstruction: Ask the candidate to walk through their design. "
        "Use the probe areas to ask follow-up questions. "
        "Reference specific components from their diagram. "
        "Be conversational but thorough."
    )

    enriched_context = "\n".join(context_parts)

    greeting = (
        "Welcome back! I've had a look at your system design on the board. "
        "Please walk me through your architecture — what are the main components "
        "and how do they interact?"
    )

    # Create new Tavus conversation with enriched context
    try:
        result = await create_conversation(
            persona_id=TAVUS_PERSONA_ID,
            replica_id=TAVUS_REPLICA_ID,
            conversation_name="system-design-discussion",
            conversational_context=enriched_context,
            custom_greeting=greeting,
        )
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Tavus API error: {e}")

    new_conv_id = result["conversation_id"]
    session["conversation_ids"].append(new_conv_id)
    session["phase"] = "discussion"

    return ResumeResponse(
        conversation_id=new_conv_id,
        conversation_url=result["conversation_url"],
    )


@app.post("/api/interview/{session_id}/end", response_model=InterviewReport)
async def end_interview(session_id: str):
    session = sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # End the active Tavus conversation
    if session["conversation_ids"]:
        last_conv_id = session["conversation_ids"][-1]
        await end_conversation(last_conv_id)

    # Generate report from full session history + diagram analysis
    report = generate_report(
        history=session["history"],
        diagram_analysis=session.get("diagram_analysis"),
    )

    session["phase"] = "ended"

    return report


# --- Preparation Endpoint ---


class PreparationRequest(BaseModel):
    job_description: str
    job_link: str | None = None
    task_type: str = "dsa"


@app.post("/api/interview/preparation", response_model=InterviewStartResponse)
def create_interview_preparation_tasks(req: PreparationRequest):
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


# --- Utterance Handler ---


@app.post("/api/tavus/utterance", response_model=TavusUtteranceResponse)
def handle_tavus_utterance(req: TavusUtteranceRequest):
    # Determine which history to use: session-based or legacy conversation-based
    if req.session_id and req.session_id in sessions:
        session = sessions[req.session_id]
        history = session["history"]

        # Inject system prompt as first message if history is empty
        if not history and session.get("system_prompt"):
            history.append({"role": "system", "content": session["system_prompt"]})

        # Track conversation_id in session
        if (
            req.conversation_id
            and req.conversation_id not in session["conversation_ids"]
        ):
            session["conversation_ids"].append(req.conversation_id)

        # If we have diagram analysis (discussion phase), add it as context
        if session.get("diagram_analysis") and session["phase"] == "discussion":
            da = session["diagram_analysis"]
            history.append(
                {
                    "role": "system",
                    "content": (
                        f"Diagram context — Components: {', '.join(da.get('components', []))}. "
                        f"Connections: {', '.join(da.get('connections', []))}. "
                        f"Probe areas: {', '.join(da.get('probe_areas', []))}."
                    ),
                }
            )
    else:
        if req.conversation_id not in conversation_history:
            conversation_history[req.conversation_id] = []
        history = conversation_history[req.conversation_id]

    # Save user utterance
    history.append({"role": "user", "content": req.utterance})

    # Run agent
    response = run_agent(history)

    # Save assistant response
    history.append({"role": "assistant", "content": response.response})

    return response


if __name__ == "__main__":
    response = run_agent([])
    print(type(response))
    print(response)
