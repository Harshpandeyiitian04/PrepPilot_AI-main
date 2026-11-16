# This file grades an interview answer and writes short feedback about what was missing.

import os
import json
from groq import Groq
from dotenv import load_dotenv
from app.agents.state import InterviewState
from app.tools.evaluation_tools import retrieve_concept_reference

# Reads the AI key from the hidden settings file.
load_dotenv()

# Scores the latest answer from 0 to 100 and moves the interview forward by one question.
def evaluation_node(state: InterviewState) -> dict:
    print("[EvaluationAgent] Evaluating answer...")

    current_question = state.get("current_question", {})
    question_text = current_question.get("question_text", "")
    topic = current_question.get("topic", "DSA")
    idx = state.get("current_question_idx", 0)
    user_answer = state.get("current_answer", "").strip()

    # If nothing was typed, the score is zero and the AI is not called.
    if not user_answer:
        score_entry = {
            "topic": topic,
            "score": 0,
            "missing_concepts": ["no answer provided"],
            "feedback": "No answer was submitted for this question."
        }
        answer_entry = {"question": question_text, "answer": "", "topic": topic}
        print(f"[EvaluationAgent] Score: 0/100 for topic {topic} (empty answer)")
        return {
            "answers": [answer_entry],
            "scores": [score_entry],
            "current_question_idx": idx + 1,
            "messages": [],
            "current_answer": ""
        }

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    # Looks up a short correct explanation so the score is based on the expected ideas.
    ref_result = retrieve_concept_reference.invoke({
        "topic": topic,
        "concept_key": question_text[:50]
    })
    reference_text = ref_result.get("reference_text", "Use general technical knowledge to evaluate.")

    prompt = f"""You are a strict but fair technical interview evaluator.

Question: {question_text}
Topic: {topic}
Reference concepts: {reference_text}
Candidate's answer: {user_answer}

Score the answer fairly based on technical correctness and completeness.
Return ONLY this JSON, no markdown, no explanation:
{{
  "score": <integer 0-100>,
  "missing_concepts": ["concept1", "concept2"],
  "feedback": "one specific sentence of constructive feedback"
}}"""

    response = client.chat.completions.create(
        model="qwen/qwen3.8-27b",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300
    )

    # Removes extra formatting the AI sometimes adds around the score.
    text = response.choices[0].message.content.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
        text = text.strip()
        if text.endswith("```"):
            text = text[:-3].strip()

    # Reads the score. If the reply is broken, a middle score of 50 is used.
    try:
        result = json.loads(text)
    except Exception as e:
        print(f"[EvaluationAgent] JSON parse failed: {e}")
        result = {"score": 50, "missing_concepts": [], "feedback": "Could not fully parse evaluation, default score given."}

    score_entry = {
        "topic": topic,
        "score": result.get("score", 50),
        "missing_concepts": result.get("missing_concepts", []),
        "feedback": result.get("feedback", "")
    }
    answer_entry = {
        "question": question_text,
        "answer": user_answer,
        "topic": topic
    }

    print(f"[EvaluationAgent] Score: {score_entry['score']}/100 for topic {topic}")

    # Saves the score, steps to the next question, and clears the answer so it is not reused.
    return {
        "answers": [answer_entry],
        "scores": [score_entry],
        "current_question_idx": idx + 1,
        "messages": [],
        "current_answer": ""
    }
