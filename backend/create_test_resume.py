# This file draws a sample resume PDF so the upload feature can be tried without a real resume.

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# Starts a new PDF page in letter size.
c = canvas.Canvas("test_resume.pdf", pagesize=letter)
c.setFont("Helvetica", 11)

# The lines of text that will appear on the sample resume.
lines = [
    "Kanav Goyal",
    "B.Tech Computer Science (2023-2027)",
    "",
    "SKILLS",
    "Python, C++, JavaScript, PostgreSQL, Redis, React, FastAPI, Next.js, LangChain",
    "",
    "PROJECTS",
    "LinkForge - URL Shortener and Analytics Platform",
    "Built a full-stack URL shortener using Next.js and Express.js with PostgreSQL",
    "for storage and Redis for caching and rate limiting. Implemented JWT auth",
    "and click analytics dashboard.",
    "",
    "InterviewOS - Multi-Agent AI Interview Platform",
    "Building a multi-agent system using LangGraph and FastAPI that conducts",
    "adaptive mock interviews, evaluates answers using LLMs, and generates",
    "personalized study plans based on performance.",
    "",
    "EXPERIENCE",
    "Competitive programmer on Codeforces, solved 300+ problems.",
]

# Writes each line a little lower than the one before it.
y = 750
for line in lines:
    c.drawString(50, y, line)
    y -= 18

# Saves the PDF and prints a note that it was created.
c.save()
print("test_resume.pdf created")
