#!/usr/bin/env python3
"""
Avaliação Humana — Agente SIH/SUS sem Guardrails
Prova de Conceito — Grupo 55

Permite que um avaliador humano interaja com o agente SEM guardrails ativos,
observando e registrando o comportamento do pipeline em modo ablação.

Uso:
    python evaluation/human_eval.py                # modo interativo sem guardrails
    python evaluation/human_eval.py --compare      # exibe resposta com E sem guardrails
    python evaluation/human_eval.py "pergunta"     # pergunta única sem guardrails
    python evaluation/human_eval.py --compare "p"  # pergunta única comparativa
"""
import argparse
import os
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from evaluation import runner


BANNER_NO_GUARDRAIL = """
╔══════════════════════════════════════════════════════════════╗
║     Avaliação Humana — Agente SIH/SUS  [SEM GUARDRAILS]     ║
║                                                              ║
║  ⚠  Os guardrails estão DESATIVADOS neste modo.             ║
║  Use para observar o comportamento do agente sem filtros.    ║
║  Digite 'sair' para encerrar.                               ║
╚══════════════════════════════════════════════════════════════╝
"""

BANNER_COMPARE = """
╔══════════════════════════════════════════════════════════════╗
║  Avaliação Humana — Comparativo COM vs SEM Guardrails        ║
║                                                              ║
║  Cada pergunta é executada duas vezes:                       ║
║    [COM]  pipeline completo com guardrails                   ║
║    [SEM]  pipeline sem guardrails (ablação)                  ║
║  Digite 'sair' para encerrar.                               ║
╚══════════════════════════════════════════════════════════════╝
"""

_SEP = "─" * 60
_WIDE = "═" * 60


def _wrap(text: str, width: int = 78, indent: int = 2) -> str:
    prefix = " " * indent
    return "\n".join(
        textwrap.fill(line, width=width, initial_indent=prefix, subsequent_indent=prefix)
        if line.strip()
        else ""
        for line in text.splitlines()
    )


def _print_result_no_guardrail(result) -> None:
    print(f"\n{_SEP}")
    print("  MODO: SEM GUARDRAILS")
    print(_SEP)

    if result.sql:
        print("\n  SQL gerado:")
        for line in result.sql.strip().splitlines():
            print(f"    {line}")

    if result.error and not result.response:
        print(f"\n  ⚠  Erro: {result.error}")
    else:
        print(f"\n  RESPOSTA DO AGENTE:")
        print(_wrap(result.response))

    if result.visualization_path:
        print(f"\n  [Visualização salva em: {result.visualization_path}]")

    print(_SEP)


def _print_result_with_guardrail(result) -> None:
    print(f"\n{_SEP}")
    print("  MODO: COM GUARDRAILS")
    print(_SEP)

    guardrail = result.guardrail_result
    if guardrail:
        valid = guardrail.get("valid")
        reason = guardrail.get("reason", "")
        status = "✅ válida" if valid else "🚫 bloqueada"
        print(f"\n  Guardrail: {status}")
        if reason:
            print(_wrap(f"Motivo: {reason}"))

    if result.sql:
        print("\n  SQL gerado:")
        for line in result.sql.strip().splitlines():
            print(f"    {line}")

    if result.error and not result.response:
        print(f"\n  ⚠  Erro: {result.error}")
    else:
        print(f"\n  RESPOSTA DO AGENTE:")
        print(_wrap(result.response))

    if result.visualization_path:
        print(f"\n  [Visualização salva em: {result.visualization_path}]")

    print(_SEP)


def _run_no_guardrail(question: str) -> None:
    print("\nExecutando pipeline sem guardrails…", flush=True)
    result = runner.run_without_guardrails(question)
    _print_result_no_guardrail(result)


def _run_compare(question: str) -> None:
    print("\n[1/2] Executando COM guardrails…", flush=True)
    result_with = runner.run_with_guardrails(question)

    print("[2/2] Executando SEM guardrails…", flush=True)
    result_without = runner.run_without_guardrails(question)

    print(f"\n{_WIDE}")
    print("  RESULTADO COMPARATIVO")
    print(_WIDE)
    _print_result_with_guardrail(result_with)
    _print_result_no_guardrail(result_without)
    print(_WIDE)


def _interactive_loop(compare: bool) -> None:
    print(BANNER_COMPARE if compare else BANNER_NO_GUARDRAIL)

    while True:
        try:
            question = input("\nPergunta: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nEncerrando…")
            break

        if not question:
            continue

        if question.lower() in ("sair", "exit", "quit"):
            print("Encerrando…")
            break

        if compare:
            _run_compare(question)
        else:
            _run_no_guardrail(question)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Avaliação humana interativa do agente SIH/SUS sem guardrails."
    )
    parser.add_argument(
        "--compare",
        action="store_true",
        help="Exibe as respostas com E sem guardrails lado a lado.",
    )
    parser.add_argument(
        "question",
        nargs="*",
        help="Pergunta única a ser executada (modo não interativo).",
    )
    args = parser.parse_args()

    if args.question:
        question = " ".join(args.question)
        if args.compare:
            print(BANNER_COMPARE)
            _run_compare(question)
        else:
            print(BANNER_NO_GUARDRAIL)
            _run_no_guardrail(question)
    else:
        _interactive_loop(compare=args.compare)


if __name__ == "__main__":
    main()
