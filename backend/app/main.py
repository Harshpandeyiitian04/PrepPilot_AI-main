import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth_routes, resume_routes, interview_routes
from app.agents.checkpointer import get_checkpointer


@asynccontextmanager
async def lifespan(_: FastAPI):
    with get_checkpointer() as checkpointer:
        checkpointer.setup()
    yield

app = FastAPI(title="InterviewOS", version="1.0.0", lifespan=lifespan)

allowed_origins = [
    origin.strip()
    for origin in os.getenv("FRONTEND_URL", "http://localhost:3000").split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router)
app.include_router(resume_routes.router)
app.include_router(interview_routes.router)

@app.get("/")
def root():
    return {"message": "InterviewOS backend is running"}

@app.get("/health")
def health():
    return {"status": "ok"}
