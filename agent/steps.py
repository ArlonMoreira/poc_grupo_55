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

from agent.config import DB_TABLES, GROQ_API_KEY, GROQ_MODEL, load_schema
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


def _parse_json_response(raw: str, fallback: dict) -> dict:
    """Strip markdown fences and parse a JSON response from the LLM."""
    clean = raw.strip()
    if clean.startswith("```"):
        lines = clean.splitlines()
        clean = "\n".join(lines[1:-1] if lines[-1].strip() == "```" else lines[1:])
    try:
        return json.loads(clean)
    except Exception:
        return fallback


# ---------------------------------------------------------------------------
# Step 0 — Question Guardrail
# ---------------------------------------------------------------------------

def guardrail_question(question: str) -> dict:
    """Validate whether the user's question is relevant to the project's domain.

    Returns a dict with keys:
        valid  (bool)
        reason (str)
    """
    system = """Você é um guardião de qualidade para um agente de análise de dados de saúde pública do SUS.

O agente é especializado EXCLUSIVAMENTE em responder perguntas sobre:
- Internações hospitalares (SIH/SUS) — dados do DATASUS, estado de Goiás
- Atendimentos ambulatoriais (SIA/SUS) — dados do DATASUS, estado de Goiás

Avalie se a pergunta do usuário é relevante para este domínio.

São perguntas VÁLIDAS:
- Perguntas sobre internações, AIHs, diagnósticos, procedimentos hospitalares, altas, óbitos hospitalares
- Perguntas sobre atendimentos ambulatoriais, consultas, procedimentos, produção ambulatorial
- Perguntas sobre custos, valores pagos, frequência ou tendências relacionadas aos dados SIH/SIA
- Perguntas sobre municípios, regiões ou estabelecimentos de saúde presentes nos dados
- Comparações entre períodos, grupos ou indicadores dentro dos dados disponíveis

São perguntas INVÁLIDAS:
- Perguntas sobre temas alheios à saúde (economia geral, política, esportes, culinária, etc.)
- Perguntas sobre dados de saúde fora do escopo SIH/SIA (vacinação, epidemiologia geral, etc.)
- Perguntas que não possam ser respondidas com dados de internações ou atendimentos ambulatoriais
- Perguntas ofensivas, sem sentido ou sem relação com o sistema de saúde

Retorne APENAS um JSON válido (sem markdown, sem texto adicional):
{
  "valid": true | false,
  "reason": "<explicação breve de por que a pergunta é válida ou inválida>"
}"""

    raw = _chat(system, f"Pergunta: {question}", temperature=0.0)
    return _parse_json_response(
        raw,
        fallback={"valid": True, "reason": "Avaliação indisponível — prosseguindo com a análise."},
    )


# ---------------------------------------------------------------------------
# Step 1 — Planner / Router
# ---------------------------------------------------------------------------

def plan(question: str) -> str:
    """Interpret the analytical intent and produce a structured action plan."""
    tables_list = "\n".join(f"- `{t}`" for t in DB_TABLES)
    system = f"""Você é um planejador analítico especializado em dados de saúde pública do SUS.

Sua função é interpretar a pergunta do usuário e definir um plano de análise claro.

Schema da base de dados (contém a descrição completa de cada tabela e seus campos):
{_get_schema()}

Tabelas disponíveis:
{tables_list}

Diretrizes para escolha de tabela(s):
- Use `public.internacoes` para perguntas sobre internações hospitalares, AIHs, diárias, alta hospitalar ou óbitos hospitalares.
- Use `public.atendimentos_ambulatorial` para perguntas sobre consultas, exames, procedimentos ambulatoriais ou produção ambulatorial.
- Use AMBAS as tabelas (com UNION ALL ou subconsultas separadas) apenas quando a pergunta exigir explicitamente uma comparação ou consolidação entre internações e ambulatorial.
- Em caso de dúvida, prefira a tabela que melhor representa a natureza assistencial descrita na pergunta.

Retorne um plano estruturado com:
1. Tabela(s) a consultar e justificativa da escolha
2. Tipo de análise (série temporal, ranking, comparação, análise territorial, custos, perfil de procedimentos, mortalidade, etc.)
3. Campos/métricas relevantes para responder à pergunta
4. Filtros necessários (período, região, CID, procedimento, etc.)
5. Agrupamentos sugeridos
6. Descrição da consulta SQL que deve ser construída

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

    tables_list = "\n".join(f"- `{t}`" for t in DB_TABLES)
    system = f"""Você é um especialista em SQL para PostgreSQL.

Com base no plano de análise e no schema da base de dados, gere uma consulta SQL válida para PostgreSQL.

Schema da base de dados:
{_get_schema()}

Tabelas disponíveis:
{tables_list}

Regras obrigatórias:
- Use SOMENTE as tabelas listadas acima; escolha a(s) indicada(s) no plano de análise
- Retorne SOMENTE a query SQL pura — sem explicações, sem markdown, sem ```sql
- Os nomes das colunas no banco são em MAIÚSCULAS (ex: N_AIH, PACIENTE_IDADE, VAL_TOT)
  Use aspas duplas ao referenciar colunas com letras maiúsculas: "N_AIH", "VAL_TOT"
- Datas: em `public.internacoes` use "DATA_INTERNACAO" e "DATA_SAIDA"; em `public.atendimentos_ambulatorial` use "PERIODO_PROCEDIMENTO"
  Para filtros e agrupamentos, aplique casting: "DATA_INTERNACAO"::date, "PERIODO_PROCEDIMENTO"::date, etc.
- "PACIENTE_OBITO": 0 = vivo, 1 = óbito (campo presente em ambas as tabelas)
- `public.internacoes` possui o identificador único "N_AIH"; `public.atendimentos_ambulatorial` não possui equivalente
- Quando usar AMBAS as tabelas, combine via UNION ALL ou subconsultas — nunca faça JOIN entre elas sem critério explícito
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
# Step 2.5 — SQL Reviewer / Corrector
# ---------------------------------------------------------------------------

def review_sql(sql: str, plan_text: str, question: str) -> dict:
    """Review the generated SQL for correctness and fix issues if found.

    Returns a dict with keys:
        corrected_sql (str)   -- the fixed query (or original if no issues)
        had_issues    (bool)  -- True when corrections were applied
        issues_found  (str)   -- description of problems found and fixes applied
    """
    tables_list = "\n".join(f"- `{t}`" for t in DB_TABLES)
    system = f"""Você é um revisor especialista em SQL para PostgreSQL, focado em dados de saúde pública do SUS.

Revise a query SQL gerada e verifique obrigatoriamente:
1. Usa SOMENTE as tabelas disponíveis: {', '.join(DB_TABLES)}
2. Nomes de colunas em MAIÚSCULAS estão entre aspas duplas (ex: "N_AIH", "VAL_TOT", "DATA_INTERNACAO")
3. Castings de data corretos: "DATA_INTERNACAO"::date, "PERIODO_PROCEDIMENTO"::date, etc.
4. A lógica da query corresponde ao plano de análise à pergunta original
5. A query é robusta para os casos de borda
6. Não há erros de sintaxe PostgreSQL (alias inválidos, funções inexistentes, etc.)
7. Há LIMIT quando a query pode retornar muitas linhas
8. Não há referências a colunas que não existem no schema

Schema da base de dados:
{_get_schema()}

Tabelas disponíveis:
{tables_list}

Se a query estiver correta, retorne-a sem alterações e marque had_issues como false.
Se houver problemas, corrija-os e descreva o que foi corrigido.

Retorne APENAS um JSON válido (sem markdown, sem texto adicional):
{{
  "corrected_sql": "<query SQL corrigida, ou original se já estiver correta>",
  "had_issues": true | false,
  "issues_found": "<descrição dos problemas encontrados e correções feitas, ou 'Nenhum problema encontrado'>"
}}"""

    raw = _chat(
        system,
        f"Query a revisar:\n{sql}\n\nPlano:\n{plan_text}\n\nPergunta original: {question}",
        temperature=0.0,
    )
    result = _parse_json_response(
        raw,
        fallback={"corrected_sql": sql, "had_issues": False, "issues_found": "Revisão indisponível — usando SQL original."},
    )

    # Strip any accidental markdown fences from the corrected SQL itself
    corrected = result.get("corrected_sql", sql).strip()
    if corrected.startswith("```"):
        lines = corrected.splitlines()
        corrected = "\n".join(lines[1:-1] if lines[-1].strip() == "```" else lines[1:])
    result["corrected_sql"] = corrected.strip() or sql

    return result


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
