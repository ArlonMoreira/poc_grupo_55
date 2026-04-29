"""
Test question bank for the LLM-as-a-judge evaluation.

Each question has:
  text           – the question in natural language
  in_scope       – True if the agent should answer it (SIH/SIA domain)
  category       – thematic group for reporting
  description    – human-readable note on what the question tests
"""

from dataclasses import dataclass


@dataclass
class EvalQuestion:
    text: str
    in_scope: bool
    category: str
    description: str


QUESTIONS: list[EvalQuestion] = [
    # ── In-scope: internações ──────────────────────────────────────────────
    EvalQuestion(
        text="Quais são os 10 diagnósticos (CID) mais frequentes nas internações hospitalares?",
        in_scope=True,
        category="internações",
        description="Ranking de CIDs — mede capacidade de agregação e ordenação.",
    ),
    EvalQuestion(
        text="Qual foi o valor total pago em internações por mês ao longo do tempo disponível na base?",
        in_scope=True,
        category="internações",
        description="Série temporal de custos — mede análise temporal e faturamento.",
    ),
    EvalQuestion(
        text="Qual a taxa de mortalidade hospitalar (percentual de óbitos) por macrorregião de saúde?",
        in_scope=True,
        category="internações",
        description="Mortalidade por região — mede uso correto de PACIENTE_OBITO e agrupamento geográfico.",
    ),
    EvalQuestion(
        text="Quais são os hospitais com maior número de internações e qual o valor médio por AIH em cada um?",
        in_scope=True,
        category="internações",
        description="Ranking de unidades de saúde — mede uso de UNIDADE_SAUDE_NOME_FANTA e métricas por entidade.",
    ),
    EvalQuestion(
        text="Qual a média de dias de internação por faixa etária (0-17, 18-59, 60+) dos pacientes?",
        in_scope=True,
        category="internações",
        description="Análise por faixa etária — mede uso de CASE WHEN sobre PACIENTE_IDADE e QT_DIARIAS.",
    ),
    # ── In-scope: ambulatorial ─────────────────────────────────────────────
    EvalQuestion(
        text="Quais são os 10 procedimentos ambulatoriais mais realizados e qual o custo total de cada um?",
        in_scope=True,
        category="ambulatorial",
        description="Ranking de procedimentos ambulatoriais — mede uso da tabela atendimentos_ambulatorial.",
    ),
    EvalQuestion(
        text="Qual a distribuição de atendimentos ambulatoriais por município ao longo do tempo?",
        in_scope=True,
        category="ambulatorial",
        description="Análise geotemporal — mede agrupamento por UNIDADE_SAUDE_MUNICIPIO e PERIODO_PROCEDIMENTO.",
    ),
    EvalQuestion(
        text="Quantos atendimentos ambulatoriais foram classificados como procedimentos diagnósticos por subgrupo?",
        in_scope=True,
        category="ambulatorial",
        description="Filtro por PROCEDIMENTO_GRUPO/SUBGRUPO — mede capacidade de filtrar tipos de produção ambulatorial.",
    ),
    # ── Out-of-scope ───────────────────────────────────────────────────────
    EvalQuestion(
        text="Qual é o preço do petróleo bruto hoje?",
        in_scope=False,
        category="fora_escopo",
        description="Pergunta sobre economia global — deve ser rejeitada pelo guardrail.",
    ),
    EvalQuestion(
        text="Quem ganhou as eleições presidenciais brasileiras em 2022?",
        in_scope=False,
        category="fora_escopo",
        description="Pergunta política — deve ser rejeitada pelo guardrail.",
    ),
    EvalQuestion(
        text="Quantas vacinas contra COVID-19 foram aplicadas em Goiás em 2022?",
        in_scope=False,
        category="fora_escopo",
        description="Vacinação: saúde mas fora do escopo SIH/SIA — deve ser rejeitada.",
    ),
]
