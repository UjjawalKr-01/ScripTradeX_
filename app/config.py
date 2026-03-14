import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "fallback-secret")
    DATABASE_PATH = os.getenv("DATABASE_PATH", "scriptradex.db")