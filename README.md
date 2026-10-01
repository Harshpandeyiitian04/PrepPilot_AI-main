# InterviewOS

### Adaptive technical interview practice, built around your experience

InterviewOS is a full-stack interview-preparation platform that turns a candidate's resume and answer history into a personalized technical interview. It combines a predictable interview strategy with AI-generated questions, answer evaluation, and focused study recommendations.

**Created and maintained by Harsh Pandey.**

[Open the live app](https://prep-pilot-ai-main.vercel.app/) · [Check API health](https://preppilot-ai-main.onrender.com/health)

## Product Overview

InterviewOS is designed to help candidates practice with questions relevant to the work and skills they actually bring to an interview.

1. **Build a candidate profile:** Upload a text-based PDF resume to extract skills, projects, and experience.
2. **Practice across topics:** Work through adaptive questions in data structures and algorithms, databases, operating systems, computer networks, OOP, and resume projects.
3. **Get actionable feedback:** Receive answer scores, feedback, and missing concepts after each response.
4. **Plan the next session:** Review topic-level performance and recommendations informed by prior sessions.

## Product Screenshots

| Candidate profile | Adaptive interview |
| --- | --- |
| ![Resume analysis screen](screenshots/Screenshot%202026-10-01%20131113.png) | ![Interview question screen](screenshots/Screenshot%202026-10-01%20131241.png) |

![InterviewOS landing page](screenshots/Screenshot%202026-10-01%20125352.png)

## Engineering Highlights

- **Multi-agent workflow:** Resume analysis, question selection, answer evaluation, and study planning are distinct responsibilities.
- **Controlled interview strategy:** Deterministic topic sequencing and difficulty decisions are separated from LLM-powered personalization.
- **Grounded evaluation:** Responses are scored against stored concept references, with topic-level performance tracked over time.
- **Persistent sessions:** LangGraph checkpoints preserve interview state across API requests.
- **Full-stack implementation:** Next.js client, FastAPI REST API, PostgreSQL persistence, JWT authentication, and a hosted LLM service.

## Architecture

```mermaid
flowchart LR
		Candidate --> Web[Next.js frontend]
		Web -->|JWT-authenticated REST| API[FastAPI backend]
		API --> Workflow[LangGraph workflows]
		Workflow --> Resume[Resume analyzer]
		Workflow --> Interview[Interview agent]
		Workflow --> Evaluation[Evaluation agent]
		Workflow --> Planner[Planner agent]
		Resume --> LLM[Groq Qwen model]
		Interview --> LLM
		Evaluation --> LLM
		Planner --> LLM
		API --> DB[(PostgreSQL)]
		Workflow --> DB
```

### Agent responsibilities

| Component | Responsibility |
| --- | --- |
| Resume analyzer | Extracts candidate skills, projects, and experience from PDF text. |
| Interview agent | Selects the next topic and question, and supports project-specific follow-ups. |
| Evaluation agent | Compares answers with concept references and produces scores and feedback. |
| Planner agent | Uses current and historical performance to recommend study priorities. |

## Technology

| Layer | Technologies |
| --- | --- |
| Frontend | Next.js App Router, React, TypeScript, Tailwind CSS |
| API | Python, FastAPI, Pydantic |
| Agent orchestration | LangGraph |
| Language model | Groq API with `qwen/qwen3.8-27b` |
| Data | PostgreSQL, LangGraph Postgres checkpointer |
| Authentication | JWT, bcrypt |
| Resume processing | PyPDF |
| Hosting | Vercel (frontend), Render (API), Supabase (PostgreSQL) |

## Repository Layout

```text
backend/
	app/agents/       Resume, interview, evaluation, and planning workflows
	app/routes/       Authentication, resume, and interview API routes
	app/tools/        PDF, question, evaluation, and persistence helpers
	app/db/           PostgreSQL schema and connection setup
	seed_questions.py Question-bank seed data
frontend/
	src/app/          Landing, authentication, resume, interview, and results pages
	src/lib/api.ts    Frontend API client
screenshots/        Product screenshots
```

## Run Locally

### Prerequisites

- Python 3.11 or newer
- Node.js 20.9 or newer
- PostgreSQL or a reachable Supabase PostgreSQL database
- A Groq API key

### 1. Configure and start the backend

From the repository root, create and activate a virtual environment, then install the dependencies:

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Set the values in `backend/.env`:

```env
DATABASE_URL=postgresql://USER:PASSWORD@HOST:5432/DATABASE
GROQ_API_KEY=your_groq_api_key
JWT_SECRET=your_long_random_secret
FRONTEND_URL=http://localhost:3000
```

URL-encode special characters in the database password, such as `@` (`%40`) and `#` (`%23`). Initialize an empty database and seed its question bank once:

```powershell
psql $env:DATABASE_URL -v ON_ERROR_STOP=1 -f app/db/schema.sql
python seed_questions.py
```

Start the API:

```powershell
uvicorn app.main:app --reload --port 8000
```

The API root is `http://localhost:8000/`; interactive documentation is at `http://localhost:8000/docs`.

### 2. Configure and start the frontend

In a second terminal:

```powershell
cd frontend
npm install
```

Create `frontend/.env.local` with the local API URL:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Start Next.js and open `http://localhost:3000`:

```powershell
npm run dev
```

## Deployment

The live deployment uses Vercel for the frontend, Render for the API, and Supabase for PostgreSQL.

### Frontend on Vercel

- Import the repository and set the project root to `frontend`.
- Set `NEXT_PUBLIC_API_URL` to `https://preppilot-ai-main.onrender.com`.
- Deploy or redeploy after setting the variable; Next.js embeds public environment variables during its build.

### Backend on Render

- Create a Web Service from the repository with `backend` as its root directory. The included Dockerfile starts Uvicorn using Render's `PORT`.
- Set `DATABASE_URL` to the Supabase PostgreSQL pooler URI, plus `GROQ_API_KEY` and a strong `JWT_SECRET`.
- Set `FRONTEND_URL` to the exact Vercel origin, without a trailing slash: `https://prep-pilot-ai-main.vercel.app`.

### Database on Supabase

Use the project's PostgreSQL connection pooler URI for `DATABASE_URL`. Apply `backend/app/db/schema.sql` once to a new database, then run `backend/seed_questions.py` once to populate the question bank. Do not rerun the seed script on an already-seeded database; it inserts additional rows.

The free Render web service may spin down while idle, so its first request after inactivity can take around a minute. The frontend and API remain available at the live links above.

## About the Creator

**InterviewOS is an original project created by Harsh Pandey.** It demonstrates end-to-end product engineering across frontend development, API design, multi-agent orchestration, model integration, authentication, PostgreSQL persistence, and cloud deployment.
