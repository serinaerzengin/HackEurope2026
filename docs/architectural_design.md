# Architecureal Design


Looking at the sequence diagram of entire interview flow, we can identify the main components and their interactions. The architecture is designed to be modular, scalable, and maintainable. 

![Sequence Diagram](https://github.com/serinaerzengin/HackEurope2026/blob/main/docs/sequence-diagram.png) 
## Technology Stack

### Backend
- **Language**: Python (v3.12+)
- **Web Framework**: FastAPI + Uvicorn (ASGI server) 
- **AI & Agents**:
  - LangChain & LangGraph (Orchestration & State)
  - LangSmith (Tracing / Observability)
  - OpenAI / Anthropic (Model provider)
  - DeepAgents (Agent Orchestration framework)
  - Firecrawl (Web crawling / scraping)
- **Database**: PostgreSQL (running via Docker)
- **Utilities**:
  - Pydantic (Validation)
  - Uvicorn (ASGI Server)
  - HTTPX & AIOHTTP (Async HTTP clients)
- **Avatar Generation**: Tavus API for video interview avatars.
- **Build Tool**: UV for managing Python environments.

### Frontend (hackeurope)
- **Framework**: Next.js 16 (App Router)
- **Library**: React 19
- **Language**: TypeScript
- **Styling**: Tailwind CSS v4, clsx, tailwind-merge
- **UI Components**: Shadcn UI, Radix UI, Lucide React (Icons)
- **Animation**: Framer Motion (motion)
- **State Management**: Jotai
- **Video / Real-time**: Daily.co (`@daily-co/daily-react`) for video calls
- **Graphics**: OGL (WebGL)

### Infrastructure
- **Containerization**: Docker & Docker Compose

#### Services
- `backend`: Python API on port 8000  
- `client`: Next.js frontend on port 3000  
- `db`: PostgreSQL 13 on port 5432  


## User Stories


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