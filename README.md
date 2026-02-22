# HackEurope2026

**Intervox** is an AI interviewer that feels real. It watches your code, reads your diagrams, challenges your decisions, and scores your performance so you can practice technical interviews under real pressure and walk into FAANG unshakable.

Intervox challenges you with **data structures & algorithms (DSA)** problems in an integrated coding environment and guides you through **system design** scenarios. Beyond solving problems, Intervox evaluates **how you think**: it analyzes time/space complexity, reviews code readability, suggests refactors, and pushes you to spot and fix bugs. Each session ends with structured scoring across **communication, problem-solving, system design, and code quality**, including a hire/no-hire style verdict and actionable improvement steps.


## Features

- **Real-time interview experience** (voice/video supported)
- **DSA coding challenges** with feedback and follow-ups
- **System design interviews** with live probing and scaling questions
- **Diagram/drawing support** for architecture solutions
- **Automated evaluation**: complexity, clarity, code quality, tradeoffs
- **Session summary report** with scores + targeted next steps
- **Company/job-context mode**: tailor interview style using job description + context

---
## Setup

### Prerequisites


- **Git**: Ensure that git is installed on your machine. [Download Git](https://git-scm.com/downloads)
- **Python 3.12+**: Required for the project. [Download Python](https://www.python.org/downloads/)
- **UV**: Used for managing Python environments. [Install UV](https://docs.astral.sh/uv/getting-started/installation/)
- **Node.js 18+**, Ensure that you have pnpm installed. [Install pnpm](https://pnpm.io/)
- **Docker** (optional): For DevContainer development. [Download Docker](https://www.docker.com/products/docker-desktop)

### Backend

```bash
cd backend
cp .env.example .env        # Fill in your API keys (see below)
uv sync
```

### Frontend

```bash
cd frontend/hackeurope
pnpm install
```

### Environment Variables

Copy `.env.example` to `.env` and fill in the required API keys:
Edit `backend/.env` with:

| Variable | Description |
|---|---|
| `ANTHROPIC_API_KEY` | Anthropic API key (for text-based interviewer) |
| `OPENAI_API_KEY` | OpenAI API key |
| `TAVUS_API_KEY` | Tavus API key (for video interview) |
| `TAVUS_PERSONA_ID` | Created via setup script (see below) |
| `TAVUS_REPLICA_ID` | Stock replica, default `r5dc7c7d0bcb` |
| `FIRECRAWL_API_KEY` | Firecrawl API key (for ingestion) |

### Tavus Persona Setup (one-time)

```bash
cd backend
uv run -m scripts.setup_persona
```

Copy the printed `persona_id` into `backend/.env` as `TAVUS_PERSONA_ID`.

## Usage

To run the application locally one of two ways:


```bash
# Backend (terminal 1)
cd backend
uv run uvicorn main:app --reload

# Frontend (terminal 2)
cd frontend/hackeurope
pnpm dev
```

Using Docker Compose:

```bash
docker compose up --build
```

Then open http://localhost:3000, pick an interview type, and start your mock interview.

There is also swagger documentation available for the backend API at http://localhost:8000/docs.



## 📖 Documentations

- [Architecture](docs/architectural_design.md)
- [Swagger API Documentation](http://localhost:8000/docs) (when running locally)
