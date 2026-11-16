# This file describes the shapes of messages the website sends to the server and gets back.

from pydantic import BaseModel, EmailStr
from typing import Optional

# The details a new person sends when they create an account.
class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    name: str

# The email and password someone sends when they log in.
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# The reply after login or signup: a login pass plus who the person is.
class AuthResponse(BaseModel):
    access_token: str
    user_id: int
    email: str
    name: str

# The answer someone sends for the current interview question.
class AnswerSubmission(BaseModel):
    session_id: int
    answer_text: str

# The reply when an interview starts: the session number and the first question.
class SessionStartResponse(BaseModel):
    session_id: int
    question: dict

# The reply after an answer: the next question, or a note that the interview is finished.
class NextQuestionResponse(BaseModel):
    session_id: int
    question: Optional[dict]
    interview_complete: bool
    score_summary: Optional[dict] = None
