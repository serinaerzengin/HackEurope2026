from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from api.routes.interview import router as interview_router

load_dotenv()

app = FastAPI(title="HackEurope2026 API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(interview_router, prefix="/api")


@app.get("/api/health")
def health():
    return {"status": "ok"}
