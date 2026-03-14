import sqlite3
import os
from dotenv import load_dotenv
load_dotenv()

DATABASE_PATH = os.getenv("DATABASE_PATH", "scriptradex.db")

def get_db():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn