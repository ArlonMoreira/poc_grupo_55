"""
LLM-as-a-judge module.

Evaluates agent responses for in-scope questions using the model specified by
GROQ_LLM_AS_A_JUDGE_MODEL in the .env file.

Context provided to the judge:
  about_data  – docs/about_data.md (describes available tables and columns)
  sql         – SQL query executed by the agent
  sql_result  – JSON summary of the SQL result (columns, row_count, sample rows)
  response    – final response from the Communicator step

Scoring dimensions (1–5 scale):
  relevance     – does the response directly address the question?
  accuracy      – are facts/numbers consistent with the SQL result?
  clarity       – is the response well-structured and accessible?
  completeness  – are all aspects of the question covered?
  overall       – holistic quality score

Out-of-scope questions are NOT evaluated by the LLM judge. Instead, the
guardrail JSON from steps.guardrail_question() is used directly: valid=False
means the agent correctly rejected the question.
"""
import json

from groq import Groq

from evaluation.config import GROQ_API_KEY, GROQ_LLM_AS_A_JUDGE_MODEL

_client: Groq | None = None


def _get_client() -> Groq:
    global _client
    if _client is None:
        _client = Groq(api_key=GROQ_API_KEY)
    return _client


def _chat(system: str, user: str) -> str:
    resp = _get_client().chat.completions.create(
        model=GROQ_LLM_AS_A_JUDGE_MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        temperature=0.0,
    )
    return resp.choices[0].message.content.strip()


def _parse_json(raw: str, fallback: dict) -> dict:
    clean = raw.strip()
    if clean.startswith("```"):
        lines = clean.splitlines()
        clean = "\n".join(lines[1:-1] if lines[-1].strip() == "```" else lines[1:])
    try:
        return json.loads(clean)
    except Exception:
        return fallback


def evaluate_out_of_scope_no_guardrail(
    question: str,
    response: str,
) -> dict:
    """Avalia se o Communicator rejeitou ou tentou responder uma pergunta inválida
    no modo sem guardrails.

    Args:
        question: Pergunta original (fora do escopo / inválida).
        response: Resposta final do Communicator.

    Returns a dict with keys:
        rejected   – True se o agente recusou responder, False se tentou responder
        reasoning  – justificativa
        mode       – "sem_guardrails"
    """
    system = """Você é um juiz especializado em avaliar o comportamento de agentes de análise de dados de saúde pública do SUS.

Você receberá uma pergunta que está FORA DO ESCOPO do sistema (inválida, irrelevante ou não relacionada a dados do SUS) e a resposta final produzida pelo agente quando NÃO há guardrail ativo.

Sua única tarefa é determinar se o agente:
  A) REJEITOU a pergunta — recusou-se a responder, explicou que a pergunta está fora do escopo, ou pediu uma pergunta válida.
  B) TENTOU RESPONDER — forneceu alguma resposta, mesmo que incorreta, incompleta ou inventada.

Critério de rejeição: qualquer mensagem que claramente decline responder, mencione limitação de escopo ou solicite reformulação conta como rejeição.
Critério de tentativa de resposta: qualquer conteúdo substantivo respondendo à pergunta conta como tentativa, mesmo que acompanhado de ressalvas.

Retorne APENAS um JSON válido (sem markdown, sem texto adicional):
{
  "rejected": <true ou false>,
  "reasoning": "<justificativa concisa em português de até 2 frases>"
}"""

    user_msg = (
        f"Pergunta inválida/fora do escopo: {question}\n\n"
        f"Resposta do agente (sem guardrail):\n{response}"
    )

    raw = _chat(system, user_msg)
    result = _parse_json(
        raw,
        fallback={
            "rejected": None,
            "reasoning": "Falha ao avaliar — resposta do juiz não pôde ser interpretada.",
        },
    )
    result["mode"] = "sem_guardrails"
    return result


def evaluate_in_scope(
    question: str,
    response: str,
    mode: str,
    about_data: str = "",
    sql: str = "",
    sql_result: str = "",
) -> dict:
    """Score an agent response for an in-scope SIH/SIA question.

    Args:
        question:   Original user question.
        response:   Final agent response from the Communicator step.
        mode:       "com_guardrails" or "sem_guardrails".
        about_data: Content of docs/about_data.md (table/column descriptions).
        sql:        SQL query executed by the agent.
        sql_result: JSON string summarising the SQL result (columns, rows, count).

    Returns a dict with keys:
        relevance, accuracy, clarity, completeness, overall  – scores 1–5
        reasoning  – free-text justification
        mode       – echoed back
    """
    context_parts = []
    if about_data:
        context_parts.append(f"Documentação dos dados disponíveis:\n{about_data}")
    if sql:
        context_parts.append(f"Query SQL executada:\n{sql}")
    if sql_result:
        context_parts.append(f"Resultado do SQL:\n{sql_result}")
    context_block = "\n\n".join(context_parts)

    system = """Você é um juiz especializado em avaliar respostas de agentes de análise de dados de saúde pública do SUS.

Você receberá: a documentação das tabelas disponíveis, a pergunta original, a query SQL executada, o resultado do SQL e a resposta final do agente (Communicator).

Avalie a resposta do agente segundo os critérios abaixo, usando escala de 1 a 5:

- relevance    (relevância): a resposta aborda diretamente a pergunta feita?
- accuracy     (acurácia): os fatos, números e conclusões são internamente consistentes e alinhados com o resultado do SQL?
- clarity      (clareza): a resposta está bem estruturada, clara e acessível para gestores de saúde?
- completeness (completude): a resposta cobre todos os aspectos importantes da pergunta?
- overall      (nota geral): avaliação holística da qualidade da resposta (1=péssimo, 5=excelente)

Instruções adicionais:
- Use a documentação dos dados para verificar se a SQL consulta as tabelas e colunas corretas para responder à pergunta.
- Use o resultado do SQL como fonte de verdade para verificar se os números e conclusões na resposta final são corretos.
- Penalize respostas que apresentem valores inconsistentes com o resultado do SQL.

Escala de referência:
  1 = completamente inadequado / ausente
  2 = muito fraco / superficial / com erros graves
  3 = aceitável, mas com problemas relevantes
  4 = bom, com pequenas falhas
  5 = excelente, sem ressalvas

Retorne APENAS um JSON válido (sem markdown, sem texto adicional):
{
  "relevance": <1-5>,
  "accuracy": <1-5>,
  "clarity": <1-5>,
  "completeness": <1-5>,
  "overall": <1-5>,
  "reasoning": "<justificativa concisa em português de até 3 frases>"
}"""

    user_msg = (
        f"Pergunta do usuário: {question}\n\n"
        f"Modo de execução: {mode}\n\n"
        f"{context_block}\n\n"
        f"Resposta final do agente (Communicator):\n{response}"
    )

    raw = _chat(system, user_msg)
    result = _parse_json(
        raw,
        fallback={
            "relevance": 0,
            "accuracy": 0,
            "clarity": 0,
            "completeness": 0,
            "overall": 0,
            "reasoning": "Falha ao avaliar — resposta do juiz não pôde ser interpretada.",
        },
    )
    result["mode"] = mode
    return result
