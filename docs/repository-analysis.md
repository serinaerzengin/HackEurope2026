# HackEurope2026 — Repository Analysis

## What We Have (Working)

### Frontend (Next.js 16 + React 19)
| File | Purpose | Status |
|------|---------|--------|
| `app/page.tsx` | Landing page — pick Coding or System Design | Working |
| `app/interview/page.tsx` | Creates Daily.co call object, calls preparation + conversation APIs, renders DailyProvider | Working |
| `components/InterviewRoom.tsx` | Renders replica video + local PiP, listens for utterances, sends to backend, echoes response | Working |
| `hooks/use-cvi-call.ts` | `joinCall` / `leaveCall` wrapping Daily.js | Working |
| `hooks/cvi-events-hooks.ts` | `useObservableEvent` + `useSendAppMessage` for Tavus events | Working |
| `lib/api.ts` | `prepareInterview()`, `createConversation()`, `sendUtterance()` | Working |
| `components/ChatWindow.tsx` | Text chat UI | Unused (leftover from text mode) |
| `components/MessageInput.tsx` | Text input UI | Unused (leftover from text mode) |

### Backend (FastAPI + Python 3.12)
| File | Purpose | Status |
|------|---------|--------|
| `main.py` | App entry, CORS, routes: `/preparation`, `/utterance`, `/health` | Working |
| `src/api/routes/tavus.py` | `POST /tavus/conversation` — creates Tavus conversation with system_prompt | Working |
| `src/api/routes/interview.py` | `POST /interview/chat` — text-based chat | Unused |
| `src/services/tavus_client.py` | Async HTTP client to Tavus API | Working |
| `src/services/interview_preperation.py` | `generate_system_prompt()` + `recommend_case()` via LangChain | Working |
| `src/services/mock_tasks.py` | Hardcoded Two Sum + URL Shortener tasks | Working (fallback) |
| `src/services/ingestion_service.py` | Firecrawl web scraping for interview questions | Implemented but **not connected** |
| `src/agents/interview_agent.py` | 5-agent evaluation pipeline (clarity, feedback, follow-ups, correctness, final) | Implemented |
| `src/db/dao.py` | Hardcoded case data (no real DB) | Stub |
| `src/scripts/setup_persona.py` | One-time Tavus persona creation | Working |
| `src/types/dto.py` | Pydantic models for requests/responses | Working |
| `src/types/cases.py` | `CaseDSAProblem`, `CaseSoftwareDesignProblem` models | Working |
| `src/evaluation/` | Empty directory | Not started |

---

## The Interview Flow (Current)

```
1. User picks interview type on landing page
2. Frontend calls POST /api/interview/preparation
   → Backend generates system_prompt via LLM + fetches hardcoded cases
3. Frontend calls POST /api/tavus/conversation (passes system_prompt)
   → Backend calls Tavus API → returns conversation_url
4. Frontend creates Daily.co call object, joins the room
5. Tavus avatar greets the user and starts the interview
6. User speaks → Tavus fires 'conversation.utterance' event
7. Frontend catches event → POST /api/tavus/utterance
8. Backend runs agent pipeline → returns response
9. Frontend sends 'conversation.echo' → avatar speaks the response
```

---

## What's Missing for a Complete Interview Simulation

### 1. The utterance endpoint returns a stub echo
**File:** `backend/main.py:55-65`

The `/api/tavus/utterance` endpoint currently returns `"I heard you say: {utterance}"`. The real agent pipeline in `interview_agent.py` exists but is **not wired in** because it uses `deepagents` which may have issues.

**To fix:** Replace the stub with the actual `run_agent()` call, or rewrite the agent pipeline using LangGraph directly.

### 2. No real database — cases are hardcoded
**File:** `backend/src/db/dao.py`

`dao.py` returns the same 2 DSA + 2 design cases every time. PostgreSQL is defined in `compose.yml` but never connected.

**To fix:** Either populate the DB and write real queries, or expand the hardcoded cases for now.

### 3. Company name is always "Google"
**File:** `backend/main.py:40`

The preparation endpoint hardcodes `company_name = "Google"` instead of extracting it from the job description.

**To fix:** Use an LLM call to extract the company name, or accept it as a frontend input.

### 4. Ingestion service is not connected
**File:** `backend/src/services/ingestion_service.py`

Firecrawl can scrape interview questions from GitHub/web, but this data never reaches the case database or the interview flow.

**To fix:** Run ingestion → store results → use in `recommend_case()`.

### 5. No conversation history / context
The utterance endpoint processes each utterance in isolation. There's no conversation history being maintained across turns.

**To fix:** Store conversation history per `conversation_id` (in-memory dict or DB) and pass full history to the agent.

### 6. No interview evaluation or scoring at the end
**Directory:** `backend/src/evaluation/` (empty)

When the interview ends, there's no summary, no score, no feedback report.

**To fix:** Build an evaluation endpoint that takes the full conversation and produces a report.

### 7. No adaptive difficulty
The system doesn't adjust question difficulty based on user performance. It asks the same cases regardless of how well the user answers.

### 8. Frontend doesn't display feedback
`InterviewRoom.tsx` receives `feedback`, `clarity_score`, `possible_follow_ups` from the backend but **only uses `response`** to echo back. The rest is thrown away.

**To fix:** Display a sidebar or overlay showing real-time feedback/scores.

---

## Priority Checklist (What to Do Next)

| # | Task | Impact | Effort |
|---|------|--------|--------|
| 1 | **Wire up `run_agent()` in the utterance endpoint** (replace stub) | Critical — without this, avatar just echoes | Medium |
| 2 | **Add conversation history tracking** (per conversation_id) | Critical — agent needs context | Low |
| 3 | **Expand case database** (more problems, better filtering) | High — more realistic interviews | Low-Medium |
| 4 | **Show feedback in frontend** (sidebar with scores/hints) | High — user needs to see evaluation | Medium |
| 5 | **Extract company name from job description** via LLM | Medium — personalization | Low |
| 6 | **Connect ingestion service** to populate cases | Medium — richer content | Medium |
| 7 | **Build end-of-interview evaluation** | Medium — complete the loop | Medium |
| 8 | **Connect PostgreSQL** for persistence | Low (for hackathon) | Medium |

---

## Quick Reference: API Endpoints

| Method | Path | Input | Output |
|--------|------|-------|--------|
| GET | `/api/health` | — | `{ status: "ok" }` |
| POST | `/api/interview/preparation` | `{ job_description, job_link?, task_type? }` | `{ system_prompt, cases[] }` |
| POST | `/api/tavus/conversation` | `{ interview_type, system_prompt? }` | `{ conversation_id, conversation_url }` |
| POST | `/api/tavus/utterance` | `{ utterance, role, conversation_id }` | `{ response, feedback?, follow_ups?, clarity_score?, correctness }` |
| POST | `/api/interview/chat` | `{ messages[], interview_type }` | `{ message }` (unused) |

---

## Key Files to Edit Next

- `backend/main.py` — Wire real agent into utterance endpoint, add conversation history
- `backend/src/agents/interview_agent.py` — Verify/fix agent pipeline works
- `backend/src/db/dao.py` — Expand cases or connect to DB
- `frontend/hackeurope/components/InterviewRoom.tsx` — Display feedback/scores
