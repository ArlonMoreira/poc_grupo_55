"""
Report generation for the LLM-as-a-judge evaluation.

Produces:
  - results/evaluation_results.json  – full raw data
  - results/evaluation_report.md     – human-readable markdown summary
"""
import json
import os
from datetime import datetime
from statistics import mean

_RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results")


def _ensure_results_dir() -> str:
    os.makedirs(_RESULTS_DIR, exist_ok=True)
    return _RESULTS_DIR


def save_raw_results(results: list[dict]) -> str:
    path = os.path.join(_ensure_results_dir(), "evaluation_results.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2, default=str)
    return path


def _score_bar(score: float, max_score: float = 5.0, width: int = 20) -> str:
    filled = round((score / max_score) * width)
    return "█" * filled + "░" * (width - filled)


def _avg(values: list) -> float:
    return round(mean(v for v in values if isinstance(v, (int, float)) and v > 0), 2) if values else 0.0


def generate_markdown_report(results: list[dict]) -> str:
    """Build and save the markdown evaluation report. Returns its file path."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    in_scope = [r for r in results if r["in_scope"]]
    out_scope = [r for r in results if not r["in_scope"]]

    lines: list[str] = [
        "# Relatório de Avaliação — LLM as a Judge",
        f"",
        f"**Data:** {now}  ",
        f"**Modelo juiz:** `{results[0].get('judge_model', 'N/A')}`  ",
        f"**Modelo agente:** `{results[0].get('agent_model', 'N/A')}`  ",
        f"**Perguntas avaliadas:** {len(results)} ({len(in_scope)} no escopo, {len(out_scope)} fora do escopo)",
        "",
        "---",
        "",
    ]

    # ── In-scope: comparison table ──────────────────────────────────────────
    lines += [
        "## 1. Perguntas no Escopo (SIH/SIA)",
        "",
        "### 1.1 Scores por pergunta",
        "",
        "| # | Pergunta | Modo | Relev. | Acurácia | Clareza | Complet. | Geral |",
        "|---|----------|------|:------:|:--------:|:-------:|:--------:|:-----:|",
    ]

    for r in in_scope:
        for mode_key, mode_label in [("com_guardrails", "c/ guardrails"), ("sem_guardrails", "s/ guardrails")]:
            scores = r.get("scores", {}).get(mode_key, {})
            q_short = r["question"][:55] + "…" if len(r["question"]) > 55 else r["question"]
            lines.append(
                f"| {r['id']} | {q_short} | {mode_label} "
                f"| {scores.get('relevance', '—')} "
                f"| {scores.get('accuracy', '—')} "
                f"| {scores.get('clarity', '—')} "
                f"| {scores.get('completeness', '—')} "
                f"| **{scores.get('overall', '—')}** |"
            )

    lines += [""]

    # ── Aggregate averages ──────────────────────────────────────────────────
    dims = ["relevance", "accuracy", "clarity", "completeness", "overall"]
    with_g = {d: _avg([r["scores"].get("com_guardrails", {}).get(d, 0) for r in in_scope]) for d in dims}
    without_g = {d: _avg([r["scores"].get("sem_guardrails", {}).get(d, 0) for r in in_scope]) for d in dims}

    lines += [
        "### 1.2 Médias por dimensão (ablation: com vs. sem guardrails)",
        "",
        "| Dimensão | Com Guardrails | Barra | Sem Guardrails | Barra | Δ (com − sem) |",
        "|----------|:--------------:|-------|:--------------:|-------|:-------------:|",
    ]
    for d in dims:
        cg = with_g[d]
        sg = without_g[d]
        delta = round(cg - sg, 2)
        delta_str = f"+{delta}" if delta >= 0 else str(delta)
        lines.append(
            f"| {d.capitalize()} "
            f"| {cg} | {_score_bar(cg)} "
            f"| {sg} | {_score_bar(sg)} "
            f"| **{delta_str}** |"
        )

    lines += [""]

    # ── Reasoning excerpts ──────────────────────────────────────────────────
    lines += [
        "### 1.3 Raciocínio do juiz (por pergunta)",
        "",
    ]
    for r in in_scope:
        lines.append(f"**Q{r['id']} — {r['question']}**")
        for mode_key, mode_label in [("com_guardrails", "Com guardrails"), ("sem_guardrails", "Sem guardrails")]:
            reasoning = r.get("scores", {}).get(mode_key, {}).get("reasoning", "N/A")
            lines.append(f"- *{mode_label}:* {reasoning}")
        lines.append("")

    # ── Out-of-scope: guardrail effectiveness ───────────────────────────────
    lines += [
        "---",
        "",
        "## 2. Perguntas Fora do Escopo (teste de guardrails)",
        "",
        "| # | Pergunta | Modo | Guardrail correto | Qualidade resp. | Raciocínio |",
        "|---|----------|------|:-----------------:|:---------------:|------------|",
    ]
    for r in out_scope:
        for mode_key, mode_label in [("com_guardrails", "c/ guardrails"), ("sem_guardrails", "s/ guardrails")]:
            scores = r.get("scores", {}).get(mode_key, {})
            q_short = r["question"][:50] + "…" if len(r["question"]) > 50 else r["question"]
            gc = "✅ Sim" if scores.get("guardrail_correct") else "❌ Não"
            rq = scores.get("response_quality", "—")
            reasoning = scores.get("reasoning", "N/A")[:120]
            lines.append(f"| {r['id']} | {q_short} | {mode_label} | {gc} | {rq} | {reasoning} |")

    # Guardrail effectiveness summary
    g_correct_with = sum(
        1 for r in out_scope if r.get("scores", {}).get("com_guardrails", {}).get("guardrail_correct", False)
    )
    g_correct_without = sum(
        1 for r in out_scope if r.get("scores", {}).get("sem_guardrails", {}).get("guardrail_correct", False)
    )
    total_oos = len(out_scope)

    lines += [
        "",
        f"**Acerto do guardrail — Com guardrails:** {g_correct_with}/{total_oos}  ",
        f"**Acerto do guardrail — Sem guardrails:** {g_correct_without}/{total_oos}  ",
        "",
    ]

    # ── Pipeline errors ─────────────────────────────────────────────────────
    errors = [r for r in results if any(
        r.get("pipeline", {}).get(mode, {}).get("error")
        for mode in ["com_guardrails", "sem_guardrails"]
    )]
    if errors:
        lines += [
            "---",
            "",
            "## 3. Erros de Pipeline",
            "",
        ]
        for r in errors:
            for mode in ["com_guardrails", "sem_guardrails"]:
                err = r.get("pipeline", {}).get(mode, {}).get("error")
                if err:
                    lines.append(f"- **Q{r['id']} ({mode}):** `{err[:200]}`")
        lines.append("")

    # ── Conclusion ──────────────────────────────────────────────────────────
    lines += [
        "---",
        "",
        "## 4. Conclusão",
        "",
        "| Métrica | Com Guardrails | Sem Guardrails |",
        "|---------|:--------------:|:--------------:|",
        f"| Média geral (perguntas no escopo) | **{with_g['overall']}** | **{without_g['overall']}** |",
        f"| Guardrails corretos (fora do escopo) | **{g_correct_with}/{total_oos}** | **{g_correct_without}/{total_oos}** |",
        "",
        "> *Relatório gerado automaticamente pelo módulo `evaluation/` do projeto poc_grupo_55.*",
    ]

    report = "\n".join(lines)
    path = os.path.join(_ensure_results_dir(), "evaluation_report.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(report)
    return path
