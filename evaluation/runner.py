"""
Agent runner variants for the evaluation ablation study.

  run_with_guardrails    – full pipeline (steps 0–6)
  run_without_guardrails – pipeline skipping step 0 (question guardrail)
                           and step 5 (verifier / guardrails)
"""
import sys
import os

# Make the project root importable when running from the evaluation dir
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from dataclasses import dataclass, field
from typing import Optional

from agent import steps
from agent.tools import execute_sql
from agent.pipeline import AnalysisResult, MAX_SQL_RETRIES, _clear_output_dir
import agent.pipeline as full_pipeline


def run_with_guardrails(question: str) -> AnalysisResult:
    """Run the complete pipeline including all guardrail steps."""
    return full_pipeline.run(question, verbose=False)


def run_without_guardrails(question: str) -> AnalysisResult:
    """Run the pipeline skipping step 0 (question guardrail) and step 5 (verifier).

    This is the ablation condition — it shows what the agent produces when
    safety checks are removed.
    """
    _clear_output_dir()
    result = AnalysisResult(question=question)

    try:
        # Step 1 — Planner / Router
        result.plan = steps.plan(question)

        # Step 2 — SQL Builder
        result.sql = steps.build_sql(result.plan, question)

        # Step 2.5 — SQL Reviewer
        sql_review = steps.review_sql(result.sql, result.plan, question)
        if sql_review.get("had_issues"):
            result.sql = sql_review["corrected_sql"]

        # Step 3 — Executor (with retries)
        for attempt in range(1, MAX_SQL_RETRIES + 1):
            result.raw_result = execute_sql(result.sql)
            if result.raw_result["success"]:
                break
            if attempt < MAX_SQL_RETRIES:
                result.sql = steps.build_sql(
                    result.plan, question, error_context=result.raw_result["error"]
                )

        if not result.raw_result["success"]:
            result.error = result.raw_result["error"]
            result.response = (
                f"Não foi possível executar a consulta após {MAX_SQL_RETRIES} tentativas.\n"
                f"Erro: {result.error}"
            )
            return result

        # Step 4 — Data Analyst
        result.analysis = steps.analyze(question, result.sql, result.raw_result)

        # Step 4.5 — Visualization
        result.visualization_path = steps.decide_and_visualize(
            question,
            result.analysis,
            result.raw_result["columns"],
            result.raw_result["rows"],
        )

        # Step 5 — SKIPPED (no verifier / guardrails)
        result.verification = "[Ablação: verificação desativada]"

        # Step 6 — Communicator (uses raw analysis instead of verified output)
        result.response = steps.communicate(question, result.analysis)

    except Exception as exc:
        result.error = str(exc)
        result.response = f"Erro inesperado: {exc}"

    return result
