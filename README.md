# HackEurope2026

AI-powered technical interview simulator with a live video avatar (Tavus CVI).

## Project Structure

```
backend/
├── main.py                  # FastAPI app, CORS, router registration
├── configuration.py         # Env var loading (API keys, Tavus config)
├── pyproject.toml           # Python dependencies
├── .env.example             # Template — copy to .env and fill in keys
├── api/routes/
│   ├── interview.py         # POST /api/interview/chat (text-based)
│   └── tavus.py             # POST /api/tavus/conversation (video interview)
├── agents/
│   └── interviewer.py       # System prompt + Claude call
├── services/
│   ├── tavus_client.py      # Async Tavus API client (create conversation)
│   └── mock_tasks.py        # Hardcoded interview tasks (coding, system-design)
├── scripts/
│   └── setup_persona.py     # One-time script to create Tavus persona
├── db/                      # Database module (future)
├── evaluation/              # Evaluation module (future)
└── ingestion_service.py     # Web crawling / content extraction (Firecrawl)

frontend/hackeurope/
├── app/
│   ├── page.tsx             # Landing page — pick interview type
│   └── interview/
│       └── page.tsx         # Video interview page (Tavus iframe)
├── components/
│   ├── ChatWindow.tsx       # Text chat message bubbles
│   ├── MessageInput.tsx     # Text input + send button
│   ├── nav-dock.tsx         # Navigation dock
│   └── ui/                  # Shared UI components
└── lib/
    ├── api.ts               # API helpers (sendMessage, createConversation)
    └── utils.ts             # Utility functions
```

## Setup

### Prerequisites

- Python 3.12+, [uv](https://docs.astral.sh/uv/)
- Node.js 18+, [pnpm](https://pnpm.io/)

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

## Running

```bash
# Backend (terminal 1)
cd backend
uv run uvicorn main:app --reload

# Frontend (terminal 2)
cd frontend/hackeurope
pnpm dev
```

Or with Docker:

```bash
docker compose up --build
```

Then open http://localhost:3000, pick an interview type, and start your mock interview.
