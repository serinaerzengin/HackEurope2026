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
These user stories outline the key features and functionalities of the Intervox interview simulation platform. The following are the finished user stories that we have implemented, along with their acceptance criteria where applicable.


### Job Application Uploader

#### User Story
As a user,  
I would like to add the job description and have the system create a similar job interview,  
So that I can get my dream job.

### Software Design Drawing Tool

#### User Story
As a user,  
I would like to be able to draw my software design solution,  
So that I can practice my software system design skills.



### Full Interview Loop Simulation

#### User Story
As a job applicant,  
I want to simulate a full interview loop (multiple rounds),  
So that I understand my overall readiness.

#### Acceptance Criteria
- Real-time voice-to-voice interaction  
- DSA (Data Structures & Algorithms) round  
- System design round  
- Summary report at the end  


### Real-Time Interactive Interviewer

#### User Story
As a user,  
I would like to get real-time questions and comments from the interviewer,  
So that it feels like a real interview.

---

### Company-Specific Interview Mode

#### User Story
As a job seeker,  
I want to simulate interviews based on job descriptions and additional context,  
So that I can get a tailored interview experience to prepare with.

#### Acceptance Criteria
- User adds company/job context  
- Behavioral questions align with company values  
- System design focus matches company scale  


### Adaptive Difficulty

#### User Story
As a candidate,  
I want the interview difficulty to adapt based on my performance,  
So that I am constantly challenged at the right level.

#### Acceptance Criteria
- System increases difficulty if the user performs well  
- System simplifies or scaffolds if the user struggles  
- Difficulty adjustments are seamless and natural  
- Feedback explains when and why difficulty changed  


### Verbal Explanation Scoring

#### User Story
As a candidate,  
I want my explanation of my solution to be evaluated,  
So that I improve my communication skills during coding interviews.

##### Acceptance Criteria
- System prompts for complexity explanation  
- AI scores clarity and correctness  
- Feedback flags missing time/space complexity analysis  
- Feedback flags lack of tradeoff discussion  



#### User Story
As a developer,  
I want to refactor poorly written code,  
So that I can improve my interview code quality skills.

##### Acceptance Criteria
- System provides messy/unreadable code  
- User rewrites for clarity and structure  
- AI evaluates readability improvements  
- Feedback includes naming, modularity, and complexity improvements  


### Live Follow-Up Design Challenges

#### User Story
As a candidate,  
I want the interviewer to challenge my system design live,  
So that I practice defending architectural decisions.

#### Acceptance Criteria
- AI asks scaling questions (“What happens at 10x traffic?”)  
- AI asks failure scenario questions  
- AI probes consistency tradeoffs  
- AI evaluates ability to justify decisions  

### User Traffic Estimation Practice

##### User Story
As a software engineer,  
I want to practice back-of-the-envelope estimations,  
So that I improve my system design fundamentals.

#### Acceptance Criteria
- System prompts for traffic calculations  
- AI checks math reasoning  
- Feedback highlights incorrect assumptions  


### Architecture Tradeoff Analyzer

#### User Story
As a user,  
I want feedback on architectural tradeoffs,  
So that I understand the strengths and weaknesses of my design.

#### Acceptance Criteria
- AI evaluates scalability, latency, cost, reliability  
- Flags missing components (cache, queue, etc.)  
- Suggests alternative architectures  
- Generates a design score  

### Confidence & Clarity Feedback

#### User Story
As a candidate,  
I want feedback on my communication clarity and confidence,  
So that I improve my interview presence.

#### Acceptance Criteria
- Detect filler phrases  
- Detect vague wording  
- Score clarity  
- Provide restructured example answer  

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