# InterviewOS

## Multi-Agent AI Interview Platform

InterviewOS is a full-stack platform for realistic, adaptive technical interview practice. It analyzes a candidate's resume, conducts a multi-topic mock interview, evaluates answers with grounded AI feedback, and turns performance history into a focused study plan.

Built and maintained by **Harsh Pandey**.

## What InterviewOS does

- Parses uploaded resumes into structured skills, projects, and experience.
- Runs adaptive interviews across DSA, DBMS, operating systems, computer networks, OOP, and resume projects.
- Chooses questions with deterministic interview strategy while using an LLM for personalized question generation and follow-ups.
- Evaluates answers against concept references and returns topic-level scores.
- Stores long-term topic performance so recommendations improve across sessions.
- Preserves active interview state between API requests with LangGraph checkpoints.

## Agent architecture

| Agent | Responsibility |
| --- | --- |
| Resume Analyzer | Extracts structured candidate information from a PDF resume. |
| Interview Agent | Selects questions and generates project-specific questions or follow-ups. |
| Evaluation Agent | Grounds answer scoring in stored concept references. |
| Planner Agent | Converts current and historical performance into study recommendations. |

The application separates deterministic interview strategy from LLM generation. This keeps topic sequencing and difficulty changes predictable while still allowing questions to reflect each candidate's real projects.

## Tech stack

- **Frontend:** Next.js App Router, TypeScript, Tailwind CSS
- **Backend:** FastAPI and Python
- **Agent orchestration:** LangGraph
- **LLM:** Groq with Llama 3.3 70B
- **Database:** PostgreSQL
- **Authentication:** JWT and bcrypt
- **Document processing:** PyPDF

## Project structure

```text
backend/     FastAPI service, agents, tools, database schema, and seed data
frontend/    Next.js application
screenshots/ Product screenshots used in the project documentation
```

## Local development

### Requirements

- Python 3.11 or newer
- Node.js 18 or newer
- PostgreSQL
- A Groq API key

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create `backend/.env`:

```env
DATABASE_URL=postgresql://your_user:your_password@localhost:5432/interviewos
GROQ_API_KEY=your_groq_api_key
JWT_SECRET=your_random_secret
```

Initialize the database and start the API:

```bash
psql -U your_user -d interviewos -f app/db/schema.sql
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000` in a browser.

## Configuration

The frontend API base URL is configured in `frontend/src/lib/api.ts`. Point it at the local FastAPI server during development or at the deployment URL for a hosted environment.

## Ownership

InterviewOS is an original project by **Harsh Pandey**.
