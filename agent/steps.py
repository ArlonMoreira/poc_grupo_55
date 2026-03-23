"""
LLM-powered steps of the analytical pipeline (all backed by Groq).

Each function corresponds to one analytical stage described in section 6.3:
  plan        → Planner / Router
  build_sql   → SQL Builder
  analyze     → Data Analyst
  verify      → Verifier / Guardrails
  communicate → Communicator
"""
import json

from groq import Groq

from agent.config import DB_TABLE, GROQ_API_KEY, GROQ_MODEL, load_schema
from agent.tools import analyze_data

_client: Groq | None = None
_schema: str | None = None


def _get_client() -> Groq:
    global _client
    if _client is None:
        _client = Groq(api_key=GROQ_API_KEY)
    return _client


def _get_schema() -> str:
    global _schema
    if _schema is None:
        _schema = load_schema()
    return _schema


def _chat(system: str, user: str, temperature: float = 0.1) -> str:
    resp = _get_client().chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        temperature=temperature,
    )
    return resp.choices[0].message.content.strip()


# ---------------------------------------------------------------------------
# Step 1 — Planner / Router
# ---------------------------------------------------------------------------

def plan(question: str) -> str:
    """Interpret the analytical intent and produce a structured action plan."""
    system = f"""Você é um planejador analítico especializado em dados de saúde pública do SUS.

Sua função é interpretar a pergunta do usuário e definir um plano de análise claro.

Schema da base de dados:
{_get_schema()}

Tabela principal: {DB_TABLE}

Retorne um plano estruturado com:
1. Tipo de análise (série temporal, ranking, comparação, análise territorial, custos, perfil de procedimentos, mortalidade, etc.)
2. Campos/métricas relevantes para responder à pergunta
3. Filtros necessários (período, região, CID, procedimento, etc.)
4. Agrupamentos sugeridos
5. Descrição da consulta SQL que deve ser construída

Seja específico e objetivo. Não gere SQL nesta etapa."""

    return _chat(system, f"Pergunta do usuário: {question}")


# ---------------------------------------------------------------------------
# Step 2 — SQL Builder
# ---------------------------------------------------------------------------

def build_sql(plan_text: str, question: str, error_context: str = "") -> str:
    """Convert the analysis plan into a valid PostgreSQL query."""
    error_note = (
        f"\n\nATENÇÃO: A query anterior falhou com o seguinte erro — corrija-o:\n{error_context}"
        if error_context
        else ""
    )

    system = f"""Você é um especialista em SQL para PostgreSQL.

Com base no plano de análise e no schema da base de dados, gere uma consulta SQL válida para PostgreSQL.

Schema da base de dados:
{_get_schema()}

Tabela: {DB_TABLE}

Regras obrigatórias:
- Use APENAS a tabela '{DB_TABLE}'
- Retorne SOMENTE a query SQL pura — sem explicações, sem markdown, sem ```sql
- Os nomes das colunas no banco são em MAIÚSCULAS (ex: N_AIH, PACIENTE_IDADE, VAL_TOT)
  Use aspas duplas ao referenciar colunas com letras maiúsculas: "N_AIH", "VAL_TOT"
- Para datas use DATE_TRUNC, EXTRACT ou filtros com casting: "DATA_INTERNACAO"::date
- PACIENTE_OBITO: 0 = vivo, 1 = óbito
- Limite resultados a {2000} linhas com LIMIT quando necessário
- Use aliases descritivos nas colunas de resultado{error_note}"""

    raw = _chat(system, f"Plano:\n{plan_text}\n\nPergunta original: {question}")

    # Strip accidental markdown fences
    sql = raw.strip()
    if sql.startswith("```"):
        lines = sql.splitlines()
        sql = "\n".join(lines[1:-1] if lines[-1].strip() == "```" else lines[1:])

    return sql.strip()


# ---------------------------------------------------------------------------
# Step 4 — Data Analyst
# ---------------------------------------------------------------------------

def analyze(question: str, sql: str, result: dict) -> str:
    """Perform descriptive analysis on the query results."""
    stats = analyze_data(result["columns"], result["rows"])

    preview = json.dumps(
        {
            "columns": result["columns"],
            "sample_rows": result["rows"][:20],
            "statistics": stats,
        },
        ensure_ascii=False,
        indent=2,
        default=str,
    )

    system = """Você é um analista de dados especializado em saúde pública.

Analise os resultados da consulta SQL e produza uma análise descritiva identificando:
- Padrões e tendências principais
- Valores mais relevantes (maiores, menores, totais)
- Comparações entre grupos quando aplicável
- Achados relevantes para gestores do SUS

Baseie-se EXCLUSIVAMENTE nos dados fornecidos. Não invente valores."""

    return _chat(
        system,
        f"Pergunta: {question}\n\nSQL executada:\n{sql}\n\nResultados:\n{preview}",
    )


# ---------------------------------------------------------------------------
# Step 5 — Verifier / Guardrails
# ---------------------------------------------------------------------------

def verify(question: str, analysis_text: str, result: dict) -> str:
    """Validate the consistency of the analysis against the raw results."""
    raw_preview = json.dumps(
        {
            "columns": result["columns"],
            "row_count": result["row_count"],
            "truncated": result["truncated"],
            "sample": result["rows"][:10],
        },
        ensure_ascii=False,
        default=str,
    )

    system = """Você é um verificador de qualidade analítica especializado em dados do SUS.

Valide a análise apresentada verificando se:
1. Todos os valores citados encontram respaldo nos dados brutos (sem alucinações)
2. Os totais, médias e contagens fazem sentido
3. O recorte analítico (período, região, filtros) está correto para a pergunta
4. Há possíveis inconsistências ou limitações a sinalizar

Se a análise estiver consistente, confirme e adicione uma nota de limitação metodológica.
Se houver problemas, sinalize claramente e corrija o que for possível."""

    return _chat(
        system,
        f"Pergunta: {question}\n\nAnálise produzida:\n{analysis_text}\n\nDados brutos (amostra):\n{raw_preview}",
    )


# ---------------------------------------------------------------------------
# Step 6 — Communicator
# ---------------------------------------------------------------------------

def communicate(question: str, verified_analysis: str) -> str:
    """Translate the validated analysis into accessible language for non-technical users."""
    system = """Você é um comunicador de dados de saúde pública do SUS.

Traduza a análise técnica em uma resposta clara e objetiva para gestores e profissionais de saúde sem formação técnica em dados.

A resposta deve:
- Responder diretamente à pergunta do usuário
- Apresentar os achados principais com os números relevantes
- Ser escrita em português, de forma profissional e acessível
- Incluir ressalvas ou limitações importantes de forma breve
- Finalizar com uma linha indicando a fonte: "Fonte: SIH/SUS — DATASUS"

Não use jargão técnico de SQL ou estatística."""

    return _chat(
        system,
        f"Pergunta original: {question}\n\nAnálise validada:\n{verified_analysis}",
        temperature=0.3,
    )
