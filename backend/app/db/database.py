# This file opens the database, which is the notebook where accounts and interviews are saved.

import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Reads the database address from the hidden settings file.
load_dotenv()

# The address of the database.
DATABASE_URL = os.getenv("DATABASE_URL")

# Opens a connection so other code can read and write saved information.
def get_connection():
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
