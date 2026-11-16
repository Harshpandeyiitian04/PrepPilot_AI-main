# This file turns the server on. The server is the helper that answers the website.

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth_routes, resume_routes, interview_routes
from app.agents.checkpointer import get_checkpointer


# When the server starts, this prepares the memory that remembers an interview in progress.
@asynccontextmanager
async def lifespan(_: FastAPI):
    with get_checkpointer() as checkpointer:
        checkpointer.setup()
    yield

# This creates the app itself and gives it the name InterviewOS.
app = FastAPI(title="InterviewOS", version="1.0.0", lifespan=lifespan)

# This builds the list of website addresses that are allowed to talk to the server.
allowed_origins = [
    origin.strip()
    for origin in os.getenv("FRONTEND_URL", "http://localhost:3000").split(",")
    if origin.strip()
]

# This opens the door so the website in the browser can call the server.
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# These attach the login, resume, and interview features to the server.
app.include_router(auth_routes.router)
app.include_router(resume_routes.router)
app.include_router(interview_routes.router)

# A simple hello message so you can see the server is running.
@app.get("/")
def root():
    return {"message": "InterviewOS backend is running"}

# A quick health check that says the server is okay.
@app.get("/health")
def health():
    return {"status": "ok"}
