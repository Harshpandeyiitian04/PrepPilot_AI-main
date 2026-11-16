# This file decides the next interview question: from the question list, about a project, or a follow-up.

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from app.agents.state import InterviewState
from app.tools.question_tools import (
    fetch_question_from_bank,
    generate_project_question,
    generate_followup_question
)

# Reads the AI key from the hidden settings file.
load_dotenv()

# The school subjects this interview can ask about.
TOPICS = ["DSA", "DBMS", "OS", "CN", "OOP"]
# The interview asks at most this many questions.
MAX_QUESTIONS = 10
# The interview tries to ask at least this many questions about the person's own projects.
MIN_PROJECT_QUESTIONS = 3
# The three ways a question can be chosen.
tools = [fetch_question_from_bank, generate_project_question, generate_followup_question]

# Picks the next subject, skipping subjects that were just used.
def get_next_topic(topics_covered: list, idx: int) -> str:
    recent = topics_covered[-3:] if len(topics_covered) >= 3 else topics_covered
    available = [t for t in TOPICS if t not in recent]
    if not available:
        available = TOPICS
    return available[idx % len(available)]

# Chooses what kind of question to ask next and tells the AI which tool to call.
def interview_node(state: InterviewState) -> dict:
    idx = state.get("current_question_idx", 0)
    scores = state.get("scores", [])
    resume_data = state.get("resume_data", {})
    projects = resume_data.get("projects", [])
    experience = resume_data.get("experience", [])
    questions_asked = state.get("questions", [])
    tool_types_used = state.get("tool_types_used", [])

    # Puts projects and past jobs in one pile so questions can be about real work.
    all_context_items = projects + [
        {
            "name": f"{e.get('role', '')} at {e.get('company', '')}",
            "description": e.get("description", "")
        }
        for e in experience
    ]

    print(f"[InterviewAgent] Deciding next question (idx: {idx})...")

    # Stops if the interview has already asked enough questions.
    if idx >= MAX_QUESTIONS:
        return {"interview_complete": True, "current_question": {}, "messages": []}

    # Looks at the last score so the next question can be easier or harder.
    last_score = scores[-1].get("score", 75) if scores else 75
    last_topic = scores[-1].get("topic", "") if scores else ""
    last_question_text = questions_asked[-1].get("question_text", "") if questions_asked else ""
    topics_covered = [q.get("topic", "") for q in questions_asked]

    if last_score < 50:
        difficulty = "easy"
    elif last_score > 80:
        difficulty = "hard"
    else:
        difficulty = "medium"

    project_questions_asked = topics_covered.count("PROJECT")
    last_tool_type = tool_types_used[-1] if tool_types_used else None
    can_do_followup = last_tool_type != "followup"

    # Makes sure project questions still get asked before the interview runs out of turns.
    questions_remaining = MAX_QUESTIONS - idx
    project_questions_still_needed = max(0, min(MIN_PROJECT_QUESTIONS, len(all_context_items)) - project_questions_asked)
    must_force_project = all_context_items and project_questions_still_needed >= questions_remaining

    asked_bank_ids = [str(q.get("id")) for q in questions_asked if q.get("id") is not None]
    asked_project_questions = [q.get("question_text", "") for q in questions_asked if q.get("topic") == "PROJECT"]

    # A low score gets a follow-up. Otherwise the interview mixes project questions with ready-made ones.
    if last_score < 50 and scores and can_do_followup:
        tool_type = "followup"
        next_topic = last_topic
    elif must_force_project or (
        all_context_items
        and project_questions_asked < min(MIN_PROJECT_QUESTIONS, len(all_context_items))
        and idx > 0
        and idx % 3 == 0
    ):
        tool_type = "project"
        next_topic = "PROJECT"
    else:
        tool_type = "bank"
        next_topic = get_next_topic(topics_covered, idx)

    # The AI is only allowed to call the question tool we already picked.
    llm = ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model="qwen/qwen3.8-27b"
    ).bind_tools(tools)

    system_prompt = "You are an interview question selector. Call exactly the tool specified. No text responses."

    if tool_type == "followup":
        user_msg = f"""Call generate_followup_question with:
- previous_question: "{last_question_text}"
- previous_answer: "answer missing core concepts"
- topic: "{next_topic}" """

    elif tool_type == "project":
        item = all_context_items[project_questions_asked % len(all_context_items)]
        exclude_str = " | ".join(asked_project_questions) if asked_project_questions else ""
        user_msg = f"""Call generate_project_question with:
- project_name: "{item['name']}"
- project_description: "{item['description']}"
- difficulty: "{difficulty}"
- exclude_questions: "{exclude_str}" """

    else:
        exclude_str = ",".join(asked_bank_ids) if asked_bank_ids else ""
        user_msg = f"""Call fetch_question_from_bank with:
- topic: "{next_topic}"
- difficulty: "{difficulty}"
- exclude_ids: "{exclude_str}" """

    print(f"[InterviewAgent] Tool: {tool_type}, Topic: {next_topic}, Difficulty: {difficulty}")

    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_msg)
    ])

    return {
        "messages": [response],
        "difficulty_level": difficulty,
        "tool_types_used": [tool_type]
    }
