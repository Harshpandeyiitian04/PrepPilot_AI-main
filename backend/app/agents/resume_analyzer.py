# This file reads a resume and pulls out skills, projects, jobs, and things the person has not covered yet.

import os
import json
from groq import Groq
from dotenv import load_dotenv
from app.agents.state import InterviewState

# Reads secret settings, including the AI key, from the hidden settings file.
load_dotenv()

# Sends the resume text to the AI and turns the reply into a simple list of skills, projects, and jobs.
def resume_analyzer_node(state: InterviewState) -> dict:
    print("[ResumeAnalyzer] Analyzing resume...")

    # Uses the resume text already saved. If none is there, a short sample resume is used.
    raw_text = state.get("resume_data", {}).get("raw_text")

    if not raw_text:
        raw_text = """
        Name: Test User
        Skills: Python, C++, PostgreSQL, Redis, React, FastAPI
        Projects:
        - LinkForge: A URL shortener with analytics, Redis caching, rate limiting, JWT auth
        Experience: B.Tech CSE student
        """

    # Asks the AI to return only a structured summary of the resume.
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    prompt = f"""You are a resume analyzer for a technical interview platform.
Analyze this resume and return ONLY a JSON object with no explanation, no markdown:
{{
  "skills": ["skill1", "skill2"],
  "projects": [
    {{"name": "project name", "description": "what it does and tech used"}}
  ],
  "experience": [
    {{"company": "company name", "role": "job title", "description": "what you built or did there and tech used"}}
  ],
  "experience_level": "student|junior|mid",
  "gaps": ["gap1", "gap2"]
}}

Rules:
- skills: extract ALL technical skills mentioned anywhere in the resume
- projects: extract all personal/academic projects
- experience: extract all internships and work experience (not projects)
- If no work experience exists, return experience as an empty array []
- experience_level: use "student" if no work experience, "junior" if 1-2 internships, "mid" if 2+ years

Resume:
{raw_text[:4000]}

Return only the raw JSON object, no code fences, no backticks."""

    response = client.chat.completions.create(
        model="qwen/qwen3.8-27b",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        max_tokens=800
    )

    # Cleans extra formatting the AI sometimes wraps around its answer.
    text = response.choices[0].message.content.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
        text = text.strip()
        if text.endswith("```"):
            text = text[:-3].strip()

    # Turns the AI text into data. If that fails, an empty summary is used so the app does not crash.
    try:
        resume_data = json.loads(text)
    except Exception as e:
        print(f"[ResumeAnalyzer] JSON parse failed: {e}")
        resume_data = {
            "skills": [],
            "projects": [],
            "experience": [],
            "experience_level": "student",
            "gaps": []
        }

    resume_data["raw_text"] = raw_text
    print(f"[ResumeAnalyzer] Extracted {len(resume_data.get('skills', []))} skills, "
          f"{len(resume_data.get('projects', []))} projects, "
          f"{len(resume_data.get('experience', []))} work experience entries")
    return {"resume_data": resume_data}
