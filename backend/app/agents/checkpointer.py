# This file connects the interview memory to the database so a session can be saved and picked up again.

import os
from dotenv import load_dotenv
from langgraph.checkpoint.postgres import PostgresSaver

# Reads the database address from the hidden settings file.
load_dotenv()

# The address of the database where interview memory is stored.
DATABASE_URL = os.getenv("DATABASE_URL")

# Hands back a saver that can store the interview's progress in the database.
def get_checkpointer():
    """
    Returns a PostgresSaver checkpointer connected to our database.
    Must call .setup() once to create the necessary tables.
    """
    return PostgresSaver.from_conn_string(DATABASE_URL)
