import os

from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_LLM_AS_A_JUDGE_MODEL = os.getenv("GROQ_LLM_AS_A_JUDGE_MODEL", "llama-3.3-70b-versatile")
