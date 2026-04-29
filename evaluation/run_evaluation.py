"""
LLM-as-a-Judge evaluation runner with ablation study.

Usage:
    python evaluation/run_evaluation.py               # evaluate all questions
    python evaluation/run_evaluation.py --ids 1 3 5   # evaluate specific question IDs
    python evaluation/run_evaluation.py --mode com_guardrails  # single mode only

Outputs (saved to evaluation/results/):
    evaluation_results.json  – full raw data
    evaluation_report.md     – human-readable report
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from evaluation.config import GROQ_LLM_AS_A_JUDGE_MODEL
from evaluation.questions import QUESTIONS
from evaluation import runner, judge, report
from agent.config import GROQ_MODEL

_ABOUT_DATA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "docs", "about_data.md"
)


def _load_about_data() -> str:
    with open(_ABOUT_DATA_PATH, encoding="utf-8") as f:
        return f.read()


def _format_sql_result(raw_result: dict) -> str:
    if not raw_result:
        return ""
    return json.dumps(
        {
            "columns": raw_result.get("columns", []),
            "row_count": raw_result.get("row_count", 0),
            "sample_rows": raw_result.get("rows", [])[:10],
            "truncated": raw_result.get("truncated", False),
        },
        ensure_ascii=False,
        indent=2,
        default=str,
    )


def _run_and_judge_question(q_id: int, q, modes: list[str], about_data: str) -> dict:
    """Run both pipeline modes and score the results for one question."""
    record: dict = {
        "id": q_id,
        "question": q.text,
        "in_scope": q.in_scope,
        "category": q.category,
        "description": q.description,
        "agent_model": GROQ_MODEL,
        "judge_model": GROQ_LLM_AS_A_JUDGE_MODEL,
        "pipeline": {},
        "scores": {},
    }

    for mode in modes:
        print(f"    [{mode}] executando pipeline…", flush=True)

        if mode == "com_guardrails":
            result = runner.run_with_guardrails(q.text)
        else:
            result = runner.run_without_guardrails(q.text)

        record["pipeline"][mode] = {
            "response": result.response,
            "sql": result.sql,
            "error": result.error,
            "guardrail_result": result.guardrail_result,
        }

        print(f"    [{mode}] avaliando…", flush=True)

        if q.in_scope:
            scores = judge.evaluate_in_scope(
                question=q.text,
                response=result.response,
                mode=mode,
                about_data=about_data,
                sql=result.sql,
                sql_result=_format_sql_result(result.raw_result),
            )
            overall = scores.get("overall", "—")
            print(f"    [{mode}] score overall: {overall}", flush=True)
        else:
            if mode == "com_guardrails" and result.guardrail_result:
                scores = {
                    "valid": result.guardrail_result.get("valid"),
                    "reason": result.guardrail_result.get("reason", ""),
                    "mode": mode,
                }
                print(f"    [{mode}] guardrail valid: {scores['valid']}", flush=True)
            else:
                # Sem guardrail: usa o LLM judge para avaliar se o Communicator
                # rejeitou ou tentou responder a pergunta inválida.
                scores = judge.evaluate_out_of_scope_no_guardrail(
                    question=q.text,
                    response=result.response,
                )
                print(f"    [{mode}] agente rejeitou: {scores.get('rejected')}", flush=True)

        record["scores"][mode] = scores

    return record


def main() -> None:
    parser = argparse.ArgumentParser(description="LLM-as-a-Judge evaluation")
    parser.add_argument(
        "--ids",
        nargs="*",
        type=int,
        help="Question IDs to evaluate (1-based). Evaluates all if omitted.",
    )
    parser.add_argument(
        "--mode",
        choices=["com_guardrails", "sem_guardrails", "ambos"],
        default="ambos",
        help="Which pipeline mode(s) to run.",
    )
    args = parser.parse_args()

    modes = (
        ["com_guardrails", "sem_guardrails"]
        if args.mode == "ambos"
        else [args.mode]
    )

    questions_to_run = (
        [(i + 1, q) for i, q in enumerate(QUESTIONS)]
        if not args.ids
        else [(i + 1, QUESTIONS[i - 1]) for i in args.ids if 1 <= i <= len(QUESTIONS)]
    )

    about_data = _load_about_data()

    print(f"\n{'=' * 60}")
    print(f"LLM-as-a-Judge — Avaliação do Agente SIH/SIA")
    print(f"Modelo agente : {GROQ_MODEL}")
    print(f"Modelo juiz   : {GROQ_LLM_AS_A_JUDGE_MODEL}")
    print(f"Modos         : {', '.join(modes)}")
    print(f"Perguntas     : {len(questions_to_run)}")
    print(f"{'=' * 60}\n")

    all_results: list[dict] = []

    for q_id, q in questions_to_run:
        scope_label = "✅ no escopo" if q.in_scope else "🚫 fora do escopo"
        print(f"\nQ{q_id} [{q.category}] {scope_label}")
        print(f"  \"{q.text}\"")

        try:
            record = _run_and_judge_question(q_id, q, modes, about_data)
            all_results.append(record)
        except Exception as exc:
            print(f"  ⚠️  Erro ao processar Q{q_id}: {exc}")
            all_results.append({
                "id": q_id,
                "question": q.text,
                "in_scope": q.in_scope,
                "category": q.category,
                "description": q.description,
                "agent_model": GROQ_MODEL,
                "judge_model": GROQ_LLM_AS_A_JUDGE_MODEL,
                "pipeline": {},
                "scores": {},
                "fatal_error": str(exc),
            })

    print(f"\n{'=' * 60}")
    print("Salvando resultados…")

    json_path = report.save_raw_results(all_results)
    md_path = report.generate_markdown_report(all_results)

    print(f"✅ JSON  → {json_path}")
    print(f"✅ Report → {md_path}")
    print(f"{'=' * 60}\n")


if __name__ == "__main__":
    main()
