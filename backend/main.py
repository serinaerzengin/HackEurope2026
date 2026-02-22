from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from src.api.routes.interview import router as interview_router
from src.api.routes.tavus import router as tavus_router
from src.types.dto import InterviewStartResponse, TavusUtteranceResponse
from src.services.interview_preperation import generate_system_prompt, recommend_case
from src.agents.interview_agent import run_agent

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


@app.post("/api/interview/preparation", response_model=InterviewStartResponse)
def create_interview_preparation_tasks(
    job_description: str, job_link: str | None = None, task_type: str = "dsa"
):
    """
    Create the initial narration of interview preparation tasks based on the job description and job link (if provided). The task type can be either "dsa" or "design".
    Args:
        job_description (str): The job description to analyze for creating interview preparation tasks.
        job_link (str | None): An optional link to the job posting for additional context.
        task_type (str): The type of tasks to create, either "dsa" for data structures and algorithms or "design" for software design problems. Default is "dsa".
    Returns:
        InterviewStartResponse: The generated interview preparation tasks.
    """

    # TODO FIND A WAY TO EXTRACT THE COMPANY NAME FROM THE JOB DESCRIPTION OR JOB LINK USING THE LLM SERVICE. For now, we are hardcoding it to "Google" for testing purposes.
    company_name = "Google"

    cases = recommend_case(
        company=company_name, job_description=job_description, task_type=task_type
    )
    system_prompt = generate_system_prompt(
        company=company_name, job_description=job_description, cases=cases
    )

    interview_response = InterviewStartResponse(
        system_prompt=system_prompt,
        cases=cases,
    )
    return interview_response


# TODO: Implement the API endpoint for handling Tavus uterences and role of who is talking (interviewer or interviewee) and return the appropriate response based on the role and the content of the utterance. This will involve integrating with the LLM service to generate responses based on the context of the conversation and the interview preparation tasks.


@app.post("/api/tavus/utterance", response_model=TavusUtteranceResponse)
def handle_tavus_utterance(utterance: str, role: str):
    history = []
    # role is either ""
    history.append({"role": role, "content": utterance})

    # TODO: start the agent chain to handle the utterance and generate a response based on the role and the content of the utterance. The agent chain should also update the history of the conversation for context in future interactions.
    response = run_agent(history)
    return response


if __name__ == "__main__":
    # check if the database is empty, if so, run the ingestion service
    # Run ingestion service to populate the database with initial data

    response = run_agent([])
    print(type(response))
    print(response)
    #
    
