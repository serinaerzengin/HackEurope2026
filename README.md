# HackEurope2026 — Intervox

**Intervox** is an AI interviewer that feels real. It watches your code, reads your diagrams, challenges your decisions, and scores your performance so you can practice technical interviews under real pressure and walk into FAANG unshakable.

Intervox challenges you with **data structures & algorithms (DSA)** problems in an integrated coding environment and guides you through **system design** scenarios. Beyond solving problems, Intervox evaluates **how you think**: it analyzes time/space complexity, reviews code readability, suggests refactors, and pushes you to spot and fix bugs. Each session ends with structured scoring across **communication, problem-solving, system design, and code quality**, including a hire/no-hire style verdict and actionable improvement steps.

---

## Features

- **Real-time interview experience** (voice/video supported)
- **DSA coding challenges** with feedback and follow-ups
- **System design interviews** with live probing and scaling questions
- **Diagram/drawing support** for architecture solutions
- **Automated evaluation**: complexity, clarity, code quality, tradeoffs
- **Session summary report** with scores + targeted next steps
- **Company/job-context mode**: tailor interview style using job description + context

---

## Tech Stack

### Backend
- **Python 3.12+**, **FastAPI**, **Uvicorn**
- **LangChain / LangGraph**, **LangSmith**
- **OpenAI / Anthropic** (LLM providers)
- **DeepAgents** (agent orchestration)
- **Firecrawl** (web crawling / ingestion)
- **PostgreSQL** (Docker)
- **Pydantic**, **HTTPX / AIOHTTP**

### Frontend
- **Next.js 16 (App Router)**, **React 19**, **TypeScript**
- **Tailwind CSS v4**, `clsx`, `tailwind-merge`
- **shadcn/ui**, **Radix UI**, **Lucide React**
- **Framer Motion**, **Jotai**
- **Daily.co** (`@daily-co/daily-react`) for real-time video
- **OGL** (WebGL)

### Infrastructure
- **Docker** + **Docker Compose**
- Services:
  - `backend` (FastAPI) on **:8000**
  - `client` (Next.js) on **:3000**
  - `db` (PostgreSQL 13) on **:5432**

---

## Setup

### Prerequisites


- **Git**: Ensure that git is installed on your machine. [Download Git](https://git-scm.com/downloads)
- **Python 3.12+**: Required for the project. [Download Python](https://www.python.org/downloads/)
- **UV**: Used for managing Python environments. [Install UV](https://docs.astral.sh/uv/gettintg-started/installation/)
- **Node.js 18+**, Ensure that you have pnpm installed. [Install pnpm](https://pnpm.io/)
- **Docker** (optional): For DevContainer development. [Download Docker](https://www.docker.com/products/docker-desktop)

### Backend
```bash
cd backend
cp .env.example .env        # Fill in your API keys (see below)
uv sync
````

### Frontend

```bash
cd frontend/hackeurope
pnpm install
```

---

## Environment Variables

Copy `backend/.env.example` to `backend/.env` and fill in:

| Variable            | Description                                |
| ------------------- | ------------------------------------------ |
| `ANTHROPIC_API_KEY` | Anthropic API key (text-based interviewer) |
| `OPENAI_API_KEY`    | OpenAI API key                             |
| `TAVUS_API_KEY`     | Tavus API key (video interview)            |
| `TAVUS_PERSONA_ID`  | Created via setup script (see below)       |
| `TAVUS_REPLICA_ID`  | Stock replica (default: `r5dc7c7d0bcb`)    |
| `FIRECRAWL_API_KEY` | Firecrawl API key (ingestion)              |

---

## Tavus Persona Setup (one-time)

```bash
cd backend
uv run -m scripts.setup_persona
```

Copy the printed `persona_id` into `backend/.env` as `TAVUS_PERSONA_ID`.

---

## Usage

### Run locally (two terminals)

```bash
# Backend (terminal 1)
cd backend
uv run uvicorn main:app --reload
```

```bash
# Frontend (terminal 2)
cd frontend/hackeurope
pnpm dev
```

Open **[http://localhost:3000](http://localhost:3000)**, pick an interview type, and start your mock interview.

Backend Swagger docs: **[http://localhost:8000/docs](http://localhost:8000/docs)**

---

## Run with Docker Compose

```bash
docker compose up --build
```

Then open **[http://localhost:3000](http://localhost:3000)**.


## Documentation

* **Architecture**: `docs/architectural_design.md`
* **API Docs (Swagger)**: [http://localhost:8000/docs](http://localhost:8000/docs) (when running locally)

