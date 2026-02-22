from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from src.api.routes.interview import router as interview_router
from src.api.routes.tavus import router as tavus_router
from src.types.dto import (
    InterviewStartResponse,
    TavusUtteranceResponse,
    TavusUtteranceRequest,
)
from src.services.interview_preperation import generate_system_prompt, recommend_case
<<<<<<< Updated upstream
from src.agents.interview_agent import run_agent
=======
from src.agents.interviewer import run_agent
>>>>>>> Stashed changes

load_dotenv()

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
    history = []
    history.append(req.model_dump())
    response = run_agent(history)

    return response


if __name__ == "__main__":
    # check if the database is empty, if so, run the ingestion service
    # Run ingestion service to populate the database with initial data

    response = run_agent([])
    print(type(response))
    print(response)
    #
    
