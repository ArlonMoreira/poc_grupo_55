#!/usr/bin/env python3
"""
Agente Inteligente SIH/SUS
Prova de Conceito — Grupo 55

Uso:
    python main.py                    # modo interativo
    python main.py "sua pergunta"     # pergunta direta via argumento
"""
import sys

from agent.pipeline import run


BANNER = """
╔══════════════════════════════════════════════════════════════╗
║        Agente Inteligente SIH/SUS — DATASUS / Goiás          ║
║  Faça perguntas em linguagem natural sobre internações        ║
║  hospitalares. Digite 'sair' para encerrar.                  ║
╚══════════════════════════════════════════════════════════════╝
"""


def main() -> None:
    print(BANNER)

    # Allow passing a one-shot question as CLI argument
    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
        result = run(question, verbose=True)
        print("\n" + "=" * 60)
        print("RESPOSTA FINAL")
        print("=" * 60)
        print(result.response)
        return

    # Interactive loop
    while True:
        try:
            question = input("\nPergunta: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nEncerrando...")
            break

        if not question:
            continue

        if question.lower() in ("sair", "exit", "quit"):
            print("Encerrando...")
            break

        result = run(question, verbose=True)

        print("\n" + "=" * 60)
        print("RESPOSTA FINAL")
        print("=" * 60)
        print(result.response)


if __name__ == "__main__":
    main()
