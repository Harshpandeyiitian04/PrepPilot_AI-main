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

## Production deployment

The application needs three hosted resources: a PostgreSQL database, a backend service, and a frontend service. Railway is suitable for PostgreSQL and the FastAPI backend; Vercel is suitable for the Next.js frontend.

### 1. Create the PostgreSQL database

1. Create a PostgreSQL service in Railway.
2. Copy its `DATABASE_URL` connection string.
3. Run the schema against that database:

```bash
psql "YOUR_DATABASE_URL" -f backend/app/db/schema.sql
```

4. Seed the question bank:

```bash
cd backend
DATABASE_URL="YOUR_DATABASE_URL" python seed_questions.py
```

Use PowerShell syntax on Windows:

```powershell
$env:DATABASE_URL = "YOUR_DATABASE_URL"
python backend/seed_questions.py
```

### 2. Deploy the backend to Railway

Create a Railway service from this repository and set its root directory to `backend`. Railway will use `railway.json` and start FastAPI on its assigned port. Add these variables to the backend service:

```env
DATABASE_URL=your_railway_postgres_url
GROQ_API_KEY=your_groq_api_key
JWT_SECRET=long_random_production_secret
FRONTEND_URL=https://your-frontend.vercel.app
```

Generate a public Railway domain and verify:

```text
https://your-backend.up.railway.app/health
```

The response should be `{"status":"ok"}`.

### 3. Deploy the frontend to Vercel

Import the repository into Vercel, set the project root directory to `frontend`, and add this environment variable before deploying:

```env
NEXT_PUBLIC_API_URL=https://your-backend.up.railway.app
```

After Vercel gives you the frontend URL, update the Railway `FRONTEND_URL` value to that exact URL and redeploy the backend.

### 4. Verify the complete system

1. Open the Vercel URL.
2. Create an account and log in.
3. Upload a PDF resume.
4. Start an interview and submit an answer.
5. Complete the interview and confirm the results page loads.
6. Check Railway logs if any request fails. The backend must have access to PostgreSQL and Groq, and the frontend URL must match `FRONTEND_URL` exactly.

## Ownership

InterviewOS is an original project by **Harsh Pandey**.
