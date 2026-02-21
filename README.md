# HackEurope2026

## Project Structure

```
backend/
├── main.py                  # FastAPI app, CORS, router registration
├── pyproject.toml           # deps: fastapi, uvicorn, anthropic, python-dotenv
├── .env.example             # copy to .env and fill in ANTHROPIC_API_KEY
├── api/
│   └── routes/
│       └── interview.py     # POST /api/interview/chat (just HTTP, no logic)
└── agents/
    ├── interviewer.py       # system prompt + Claude call
    └── agentexample.py      # dummy placeholder for new agents

frontend/hackeurope/
├── app/
│   ├── page.tsx             # landing page with "Start Interview" button
│   └── interview/
│       └── page.tsx         # chat UI, auto-starts interview on load
├── components/
│   ├── ChatWindow.tsx       # renders message bubbles
│   └── MessageInput.tsx     # text input + send button
└── lib/
    └── api.ts               # sendMessage() fetch wrapper
```

## To run

```bash
# Backend
cd backend
cp .env.example .env        # add your ANTHROPIC_API_KEY
uv sync
uv run uvicorn main:app --reload

# Frontend
cd frontend/hackeurope
cp .env.local.example .env.local
pnpm dev
```