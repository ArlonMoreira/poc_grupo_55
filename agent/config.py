import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Database
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER", "datasus")
DB_PASSWORD = os.getenv("DB_PASSWORD", "datasus")
DB_NAME = os.getenv("DB_NAME", "datasus")
DB_TABLES = ["public.internacoes", "public.atendimentos_ambulatorial"]

# Groq
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

_SCHEMA_PATH = Path(__file__).parent.parent / "docs" / "about_data.md"


def load_schema() -> str:
    return _SCHEMA_PATH.read_text(encoding="utf-8")
