"""
Orchestrates the full analytical pipeline described in section 6.3:

  1. Planner/Router   → interprets the user's question
  2. SQL Builder      → generates a PostgreSQL query
  3. Executor         → runs the query (with one automatic retry on error)
  4. Data Analyst     → descriptive analysis of the results
  5. Verifier         → consistency check / guardrails
  6. Communicator     → accessible final response
"""
from dataclasses import dataclass, field
from typing import Optional

from agent import steps
from agent.tools import execute_sql


@dataclass
class AnalysisResult:
    question: str
    plan: str = ""
    sql: str = ""
    raw_result: dict = field(default_factory=dict)
    analysis: str = ""
    verification: str = ""
    response: str = ""
    error: Optional[str] = None


def run(question: str, verbose: bool = True) -> AnalysisResult:
    """Run the full pipeline for a natural-language question.

    Args:
        question: The user's question in natural language.
        verbose:  When True, prints each step's output to stdout.

    Returns:
        An AnalysisResult with all intermediate outputs and the final response.
    """
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
        # Step 3 — Executor  (with one automatic retry on SQL error)
        # ------------------------------------------------------------------
        result.raw_result = execute_sql(result.sql)

        if not result.raw_result["success"]:
            log("EXECUTOR", f"SQL error: {result.raw_result['error']} — retrying with error context...")
            result.sql = steps.build_sql(result.plan, question, error_context=result.raw_result["error"])
            log("SQL BUILDER (retry)", result.sql)
            result.raw_result = execute_sql(result.sql)

        if not result.raw_result["success"]:
            result.error = result.raw_result["error"]
            result.response = (
                f"Não foi possível executar a consulta após duas tentativas.\n"
                f"Erro: {result.error}"
            )
            log("EXECUTOR", f"Final error: {result.error}")
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
