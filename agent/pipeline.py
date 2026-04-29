"""
Orchestrates the full analytical pipeline described in section 6.3:

  0. Question Guardrail → validates question relevance to SIH/SIA domain
  1. Planner/Router     → interprets the user's question
  2. SQL Builder        → generates a PostgreSQL query
  2.5 SQL Reviewer      → validates and corrects the generated SQL
  3. Executor           → runs the query (with automatic retries on error)
  4. Data Analyst       → descriptive analysis of the results
  5. Verifier           → consistency check / guardrails
  6. Communicator       → accessible final response
"""
import glob
import os
from dataclasses import dataclass, field
from typing import Optional

from agent import steps
from agent.tools import execute_sql


OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
MAX_SQL_RETRIES = 3


def _clear_output_dir() -> None:
    """Remove all files inside the output directory before a new question."""
    if not os.path.isdir(OUTPUT_DIR):
        return
    for file_path in glob.glob(os.path.join(OUTPUT_DIR, "*")):
        if os.path.isfile(file_path):
            os.remove(file_path)


@dataclass
class AnalysisResult:
    question: str
    plan: str = ""
    sql: str = ""
    raw_result: dict = field(default_factory=dict)
    analysis: str = ""
    visualization_path: Optional[str] = None
    verification: str = ""
    response: str = ""
    error: Optional[str] = None
    guardrail_result: dict = field(default_factory=dict)


def run(question: str, verbose: bool = True) -> AnalysisResult:
    """Run the full pipeline for a natural-language question.

    Args:
        question: The user's question in natural language.
        verbose:  When True, prints each step's output to stdout.

    Returns:
        An AnalysisResult with all intermediate outputs and the final response.
    """
    _clear_output_dir()
    result = AnalysisResult(question=question)

    def log(step: str, content: str) -> None:
        if not verbose:
            return
        preview = content[:600] + "\n[...truncated]" if len(content) > 600 else content
        print(f"\n{'=' * 60}")
        print(f"[{step}]")
        print(preview)

    try:
        # ------------------------------------------------------------------
        # Step 0 — Question Guardrail
        # ------------------------------------------------------------------
        guardrail = steps.guardrail_question(question)
        result.guardrail_result = guardrail
        log(
            "GUARDRAIL (pergunta)",
            f"Válida: {guardrail.get('valid')} — {guardrail.get('reason')}",
        )
        if not guardrail.get("valid", True):
            result.error = "Pergunta fora do escopo do agente."
            result.response = (
                f"Sua pergunta está fora do escopo deste agente.\n\n"
                f"{guardrail.get('reason', '')}\n\n"
                f"Este agente responde exclusivamente perguntas sobre internações hospitalares "
                f"(SIH/SUS) e atendimentos ambulatoriais (SIA/SUS) do DATASUS — Goiás."
            )
            return result

        # ------------------------------------------------------------------
        # Step 1 — Planner / Router
        # ------------------------------------------------------------------
        result.plan = steps.plan(question)
        log("PLANNER", result.plan)

        # ------------------------------------------------------------------
        # Step 2 — SQL Builder
        # ------------------------------------------------------------------
        result.sql = steps.build_sql(result.plan, question)
        log("SQL BUILDER", result.sql)

        # ------------------------------------------------------------------
        # Step 2.5 — SQL Reviewer / Corrector
        # ------------------------------------------------------------------
        sql_review = steps.review_sql(result.sql, result.plan, question)
        if sql_review.get("had_issues"):
            log(
                "SQL REVIEWER",
                f"Problemas encontrados e corrigidos:\n{sql_review['issues_found']}\n\nSQL corrigido:\n{sql_review['corrected_sql']}",
            )
            result.sql = sql_review["corrected_sql"]
        else:
            log("SQL REVIEWER", f"SQL validado sem problemas. {sql_review.get('issues_found', '')}")

        # ------------------------------------------------------------------
        # Step 3 — Executor  (with automatic retries on SQL error)
        # ------------------------------------------------------------------
        for attempt in range(1, MAX_SQL_RETRIES + 1):
            result.raw_result = execute_sql(result.sql)
            if result.raw_result["success"]:
                break
            log(
                "EXECUTOR",
                f"Tentativa {attempt}/{MAX_SQL_RETRIES} falhou — Erro: {result.raw_result['error']}",
            )
            if attempt < MAX_SQL_RETRIES:
                result.sql = steps.build_sql(
                    result.plan, question, error_context=result.raw_result["error"]
                )
                log(f"SQL BUILDER (tentativa {attempt + 1})", result.sql)

        if not result.raw_result["success"]:
            result.error = result.raw_result["error"]
            result.response = (
                f"Não foi possível executar a consulta após {MAX_SQL_RETRIES} tentativas.\n"
                f"Erro: {result.error}"
            )
            log("EXECUTOR", f"Erro final após {MAX_SQL_RETRIES} tentativas: {result.error}")
            return result

        log(
            "EXECUTOR",
            f"Returned {result.raw_result['row_count']} rows. "
            f"Columns: {result.raw_result['columns']}"
            + (" [TRUNCATED]" if result.raw_result["truncated"] else ""),
        )

        # ------------------------------------------------------------------
        # Step 4 — Data Analyst
        # ------------------------------------------------------------------
        result.analysis = steps.analyze(question, result.sql, result.raw_result)
        log("ANALYST", result.analysis)

        # ------------------------------------------------------------------
        # Step 4.5 — Visualization (decide + generate)
        # ------------------------------------------------------------------
        result.visualization_path = steps.decide_and_visualize(
            question,
            result.analysis,
            result.raw_result["columns"],
            result.raw_result["rows"],
        )
        if result.visualization_path:
            log("VISUALIZER", f"Imagem gerada: {result.visualization_path}")
        else:
            log("VISUALIZER", "Nenhuma visualização gerada para esta consulta.")

        # ------------------------------------------------------------------
        # Step 5 — Verifier / Guardrails
        # ------------------------------------------------------------------
        result.verification = steps.verify(question, result.analysis, result.raw_result)
        log("VERIFIER", result.verification)

        # ------------------------------------------------------------------
        # Step 6 — Communicator
        # ------------------------------------------------------------------
        result.response = steps.communicate(question, result.verification)
        log("COMMUNICATOR", result.response)

    except Exception as exc:
        result.error = str(exc)
        result.response = f"Erro inesperado no pipeline: {exc}"
        if verbose:
            print(f"\n[ERROR] {exc}")

    return result
