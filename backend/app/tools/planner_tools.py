# This file loads a person's older subject scores so the study plan can use them.

import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from langchain_core.tools import tool

# Reads the database address from the hidden settings file.
load_dotenv()

# Opens a database connection that returns each row like a labeled dictionary.
def get_conn():
    return psycopg2.connect(os.getenv("DATABASE_URL"), cursor_factory=RealDictCursor)

# Gets past averages for one person, weakest subjects first. The note below is also read by the AI tool.
@tool
def fetch_long_term_performance(user_id: int) -> dict:
    """Fetch the user's long-term topic performance across all past sessions.
    Use this to factor historical weaknesses into the study plan.
    Returns rolling average scores per topic.
    """
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT topic, rolling_average_score, attempt_count, last_attempted
            FROM user_topic_performance
            WHERE user_id = %s
            ORDER BY rolling_average_score ASC
            """,
            (user_id,)
        )
        rows = cur.fetchall()
        cur.close()
        conn.close()
        if rows:
            return {"performance": [dict(r) for r in rows]}
        return {"performance": [], "message": "No history yet — this is the user's first session."}
    except Exception as e:
        return {"performance": [], "error": str(e)}
