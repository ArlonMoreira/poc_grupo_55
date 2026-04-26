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

DEFAULT_TABLE = "internacoes"
AVAILABLE_TABLES = ("internacoes", "atendimentos_ambulatorial")

# Groq
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

_DOCS_DIR = Path(__file__).parent.parent / "docs"
_SCHEMA_PATHS = {
    "internacoes": _DOCS_DIR / "about_data_internacoes.md",
    "atendimentos_ambulatorial": _DOCS_DIR / "about_data_ambulatorial.md",
}

TABLE_CONTEXT = {
    "internacoes": {
        "description": (
            "Contexto hospitalar com AIH e internação. "
            "Inclui permanência hospitalar, alta, óbito hospitalar e custos de internação."
        ),
        "examples": (
            "internação, AIH, diária, tempo de permanência, alta hospitalar, "
            "óbitos em internação, custo de internação"
        ),
    },
    "atendimentos_ambulatorial": {
        "description": (
            "Contexto ambulatorial sem internação. "
            "Inclui consultas, exames, procedimentos ambulatoriais e produção ambulatorial."
        ),
        "examples": (
            "ambulatório, atendimento ambulatorial, consulta, produção ambulatorial, "
            "procedimento ambulatorial, APAC/BPA"
        ),
    },
}


def load_schema(table_name: str = DEFAULT_TABLE) -> str:
    schema_path = _SCHEMA_PATHS.get(table_name, _SCHEMA_PATHS[DEFAULT_TABLE])
    if not schema_path.exists():
        return (
            f"Schema documental não encontrado para a tabela '{table_name}'. "
            "Mantenha a query simples e baseada apenas em colunas conhecidas no banco."
        )
    return schema_path.read_text(encoding="utf-8")
