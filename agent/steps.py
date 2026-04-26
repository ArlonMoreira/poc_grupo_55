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

from agent.config import (
    AVAILABLE_TABLES,
    DEFAULT_TABLE,
    GROQ_API_KEY,
    GROQ_MODEL,
    TABLE_CONTEXT,
    load_schema,
)
from agent.tools import analyze_data, generate_visualization

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
# Step 0 — Table Selector
# ---------------------------------------------------------------------------

def route_table(question: str) -> str:
    """Decide qual tabela usar com base no contexto da pergunta."""
    table_guide = "\n".join(
        [
            f"- {name}: {meta['description']} | exemplos: {meta['examples']}"
            for name, meta in TABLE_CONTEXT.items()
        ]
    )

    system = f"""Você é um roteador semântico de consultas de saúde pública.
Escolha exatamente UMA tabela alvo para a pergunta do usuário.

Tabelas disponíveis:
{table_guide}

Retorne APENAS um JSON válido:
{{"table": "<nome_da_tabela>", "reason": "<justificativa_curta>"}}

Regras:
- "table" deve ser uma entre: {", ".join(AVAILABLE_TABLES)}
- Se a pergunta for ambígua, use "{DEFAULT_TABLE}".
- Não inclua markdown, nem texto fora do JSON.
"""

    raw = _chat(system, f"Pergunta: {question}", temperature=0.0).strip()
    if raw.startswith("```"):
        lines = raw.splitlines()
        raw = "\n".join(lines[1:-1] if lines[-1].strip() == "```" else lines[1:])

    try:
        parsed = json.loads(raw)
        selected = parsed.get("table", DEFAULT_TABLE)
    except Exception:
        selected = DEFAULT_TABLE

    if selected not in AVAILABLE_TABLES:
        selected = DEFAULT_TABLE

    return selected

# ---------------------------------------------------------------------------
# Step 1 — Planner / Router
# ---------------------------------------------------------------------------

def plan(question: str, table_name: str, sample_context: dict | None = None) -> str:
    """Interpret the analytical intent and produce a structured action plan."""
    sample_preview = "Amostra indisponível."
    if sample_context and sample_context.get("success"):
        payload = {
            "columns": sample_context.get("columns", []),
            "sample_rows": sample_context.get("rows", [])[:5],
        }
        sample_preview = json.dumps(payload, ensure_ascii=False, default=str, indent=2)

    system = f"""Você é um planejador analítico especializado em dados de saúde pública do SUS.

Sua função é interpretar a pergunta do usuário e definir um plano de análise claro.

Schema da base de dados: {load_schema(table_name)}

Tabela principal: {table_name}

Amostra real da tabela (use para inferir formatos e padrões):
{sample_preview}

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

def build_sql(
    plan_text: str,
    question: str,
    table_name: str,
    sample_context: dict | None = None,
    error_context: str = "",
) -> str:
    """Convert the analysis plan into a valid PostgreSQL query."""
    sample_preview = "Amostra indisponível."
    if sample_context and sample_context.get("success"):
        payload = {
            "columns": sample_context.get("columns", []),
            "sample_rows": sample_context.get("rows", [])[:5],
        }
        sample_preview = json.dumps(payload, ensure_ascii=False, default=str, indent=2)

    error_note = (
        f"\n\nATENÇÃO: A query anterior falhou com o seguinte erro — corrija-o:\n{error_context}"
        if error_context
        else ""
    )

    system = f"""Você é um especialista em SQL para PostgreSQL.

Com base no plano de análise e no schema da base de dados, gere uma consulta SQL válida para PostgreSQL.

Schema da base de dados: {load_schema(table_name)}

Tabela: {table_name}

Amostra real da tabela (use para inferir formatos e padrões):
{sample_preview}

Regras obrigatórias:
- Use APENAS a tabela '{table_name}'
- Use a amostra para inferir se campos de data estão como texto; quando necessário, use cast ::date.
- Use a amosra pra você entender o tipo de dado de cada coluna e como os dados estão sendo apresentados para fazer corretamente a consulta sql.
- Em filtros textuais, prefira ILIKE (case-insensitive).
- Não assuma colunas que não aparecem no schema/amostra.
- Leve em consideração as assentuações como "diagnóstico por radiologia" ao invés de "diagnostico por radiologia"
- Quando a pergunta mencionar tipos de exame/procedimento (ex.: tomografia, ultrassonografia, teste rápido, laboratório),
  priorize filtro por "PROCEDIMENTO_SUBGRUPO"; use "PROCEDIMENTO_GRUPO" e "PROCEDIMENTO_DESCRICAO" como complemento.
- Retorne SOMENTE a query SQL pura — sem explicações, sem markdown, sem ```sql
- Os nomes das colunas no banco são em MAIÚSCULAS (ex: N_AIH, PACIENTE_IDADE, VAL_TOT)
  Use aspas duplas ao referenciar colunas com letras maiúsculas: "N_AIH", "VAL_TOT"
- Para busca textual sem sensibilidade a maiúsculas/minúsculas, prefira ILIKE.
- Se usar LIKE em campos textuais, normalize obrigatoriamente com UPPER(...) ou LOWER(...):
  Exemplo: UPPER("PROCEDIMENTO_DESCRICAO") LIKE UPPER('%consulta%')
- Para qualquer coluna de data que esteja como texto, faça cast explícito antes de usar funções de data.
  Exemplos válidos:
  - EXTRACT(YEAR FROM "PERIODO_PROCEDIMENTO"::date)
  - DATE_TRUNC('month', "PERIODO_PROCEDIMENTO"::date)
  - "PERIODO_PROCEDIMENTO"::date BETWEEN DATE '2023-01-01' AND DATE '2023-12-31'
- Em perguntas de total (ex.: "quantas consultas"), retorne um único agregado principal (COUNT/SUM)
  e evite GROUP BY desnecessário, salvo quando o usuário pedir detalhamento por mês, município, CID etc.
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
# Step 4.5 — Visualization Decider + Generator
# ---------------------------------------------------------------------------

def decide_and_visualize(question: str, analysis: str, columns: list, rows: list) -> str | None:
    """Ask the LLM if a chart or table would be useful, then generate it.

    Returns the absolute path to the generated PNG, or None when not applicable.
    """
    sample = json.dumps(
        {"columns": columns, "sample_rows": rows[:5]},
        ensure_ascii=False,
        default=str,
    )

    system = """Você é um especialista em visualização de dados de saúde pública.

Analise a pergunta, a análise textual e a amostra dos dados e decida se seria útil gerar
um gráfico ou tabela visual para complementar a resposta.

Retorne APENAS um JSON válido com a seguinte estrutura (sem texto adicional, sem markdown):
{
  "type": "bar" | "horizontal_bar" | "line" | "pie" | "table" | "none",
  "x_column": "<nome exato da coluna para categorias / eixo X>",
  "y_column": "<nome exato da coluna numérica para valores / eixo Y>",
  "title": "<título descritivo para o gráfico>",
  "reason": "<justificativa breve>"
}

Diretrizes de escolha:
- "bar"            → ranking ou comparação com até 15 categorias de nome curto
- "horizontal_bar" → ranking com nomes longos (procedimentos, municípios, CIDs)
- "line"           → série temporal (meses, trimestres, anos em sequência)
- "pie"            → proporções com no máximo 6 categorias
- "table"          → resultado com múltiplas colunas relevantes e ≤ 20 linhas
- "none"           → dado único, texto livre ou visualização não agrega valor

x_column e y_column DEVEM ser nomes exatos presentes no campo "columns" da amostra.
Para "table", preencha x_column e y_column com strings vazias."""

    raw = _chat(
        system,
        f"Pergunta: {question}\n\nAnálise:\n{analysis}\n\nDados (amostra):\n{sample}",
        temperature=0.0,
    )

    # Parse the LLM JSON response
    try:
        clean = raw.strip()
        if clean.startswith("```"):
            lines = clean.splitlines()
            clean = "\n".join(lines[1:-1] if lines[-1].strip() == "```" else lines[1:])
        viz_decision = json.loads(clean)
    except Exception:
        return None

    return generate_visualization(columns, rows, viz_decision)


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
