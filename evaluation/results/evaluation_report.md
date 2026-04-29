# Relatório de Avaliação — LLM as a Judge

**Data:** 2026-04-28 23:56  
**Modelo juiz:** `openai/gpt-oss-120b`  
**Modelo agente:** `llama-3.3-70b-versatile`  
**Perguntas avaliadas:** 11 (8 no escopo, 3 fora do escopo)

---

## 1. Perguntas no Escopo (SIH/SIA)

### 1.1 Scores por pergunta

| # | Pergunta | Modo | Relev. | Acurácia | Clareza | Complet. | Geral |
|---|----------|------|:------:|:--------:|:-------:|:--------:|:-----:|
| 1 | Quais são os 10 diagnósticos (CID) mais frequentes nas … | c/ guardrails | 5 | 2 | 4 | 3 | **3** |
| 1 | Quais são os 10 diagnósticos (CID) mais frequentes nas … | s/ guardrails | 1 | 1 | 2 | 1 | **1** |
| 2 | Qual foi o valor total pago em internações por mês ao l… | c/ guardrails | 1 | 1 | 1 | 1 | **1** |
| 2 | Qual foi o valor total pago em internações por mês ao l… | s/ guardrails | 1 | 1 | 1 | 1 | **1** |
| 3 | Qual a taxa de mortalidade hospitalar (percentual de ób… | c/ guardrails | 1 | 1 | 1 | 1 | **1** |
| 3 | Qual a taxa de mortalidade hospitalar (percentual de ób… | s/ guardrails | 1 | 1 | 2 | 1 | **1** |
| 4 | Quais são os hospitais com maior número de internações … | c/ guardrails | 1 | 1 | 1 | 1 | **1** |
| 4 | Quais são os hospitais com maior número de internações … | s/ guardrails | 1 | 1 | 1 | 1 | **1** |
| 5 | Qual a média de dias de internação por faixa etária (0-… | c/ guardrails | 1 | 1 | 1 | 1 | **1** |
| 5 | Qual a média de dias de internação por faixa etária (0-… | s/ guardrails | 1 | 1 | 2 | 1 | **1** |
| 6 | Quais são os 10 procedimentos ambulatoriais mais realiz… | c/ guardrails | 1 | 1 | 2 | 1 | **1** |
| 6 | Quais são os 10 procedimentos ambulatoriais mais realiz… | s/ guardrails | 1 | 1 | 1 | 1 | **1** |
| 7 | Qual a distribuição de atendimentos ambulatoriais por m… | c/ guardrails | 1 | 1 | 1 | 1 | **1** |
| 7 | Qual a distribuição de atendimentos ambulatoriais por m… | s/ guardrails | 1 | 1 | 1 | 1 | **1** |
| 8 | Quantos atendimentos ambulatoriais foram classificados … | c/ guardrails | 1 | 1 | 1 | 1 | **1** |
| 8 | Quantos atendimentos ambulatoriais foram classificados … | s/ guardrails | 1 | 1 | 1 | 1 | **1** |

### 1.2 Médias por dimensão (ablation: com vs. sem guardrails)

| Dimensão | Com Guardrails | Barra | Sem Guardrails | Barra | Δ (com − sem) |
|----------|:--------------:|-------|:--------------:|-------|:-------------:|
| Relevance | 1.5 | ██████░░░░░░░░░░░░░░ | 1 | ████░░░░░░░░░░░░░░░░ | **+0.5** |
| Accuracy | 1.12 | ████░░░░░░░░░░░░░░░░ | 1 | ████░░░░░░░░░░░░░░░░ | **+0.12** |
| Clarity | 1.5 | ██████░░░░░░░░░░░░░░ | 1.38 | ██████░░░░░░░░░░░░░░ | **+0.12** |
| Completeness | 1.25 | █████░░░░░░░░░░░░░░░ | 1 | ████░░░░░░░░░░░░░░░░ | **+0.25** |
| Overall | 1.25 | █████░░░░░░░░░░░░░░░ | 1 | ████░░░░░░░░░░░░░░░░ | **+0.25** |

### 1.3 Raciocínio do juiz (por pergunta)

**Q1 — Quais são os 10 diagnósticos (CID) mais frequentes nas internações hospitalares?**
- *Com guardrails:* A resposta lista 10 CID, atendendo à pergunta, mas os valores parecem inventados e não há indicação de período ou fonte detalhada, comprometendo a acurácia; a apresentação é clara, porém falta contextualização completa.
- *Sem guardrails:* A resposta não fornece nenhum dos diagnósticos solicitados, apresentando apenas um erro de taxa de uso, portanto não atende à pergunta nem demonstra acurácia ou completude.

**Q2 — Qual foi o valor total pago em internações por mês ao longo do tempo disponível na base?**
- *Com guardrails:* A resposta não fornece nenhum dado sobre o valor total pago em internações por mês, apresentando apenas um erro de taxa de uso, portanto não atende à pergunta.
- *Sem guardrails:* A resposta não fornece nenhum dado sobre o valor total pago em internações por mês, apresentando apenas um erro de taxa de uso, portanto não atende à pergunta.

**Q3 — Qual a taxa de mortalidade hospitalar (percentual de óbitos) por macrorregião de saúde?**
- *Com guardrails:* A resposta não fornece nenhum dado ou análise sobre a taxa de mortalidade hospitalar por macrorregião, apresentando apenas um erro de limite de taxa, portanto não atende à pergunta.
- *Sem guardrails:* A resposta não fornece nenhum dado ou análise sobre a taxa de mortalidade hospitalar por macrorregião, apresentando apenas um erro de limite de taxa, portanto não atende à pergunta.

**Q4 — Quais são os hospitais com maior número de internações e qual o valor médio por AIH em cada um?**
- *Com guardrails:* A resposta não fornece nenhum dado sobre hospitais, internações ou valores de AIH, apresentando apenas um erro de taxa de uso, portanto não atende à pergunta.
- *Sem guardrails:* A resposta não fornece nenhum dado sobre hospitais, internações ou valores de AIH, apresentando apenas um erro de taxa. Não atende à pergunta, carece de conteúdo e não é útil.

**Q5 — Qual a média de dias de internação por faixa etária (0-17, 18-59, 60+) dos pacientes?**
- *Com guardrails:* A resposta não fornece nenhum dado ou análise sobre a média de dias de internação por faixa etária, apresentando apenas um erro de taxa de limite, portanto falha em todos os critérios.
- *Sem guardrails:* A resposta não fornece nenhum dado ou análise sobre a média de dias de internação por faixa etária, apresentando apenas um erro de taxa de uso, portanto não atende à pergunta.

**Q6 — Quais são os 10 procedimentos ambulatoriais mais realizados e qual o custo total de cada um?**
- *Com guardrails:* A resposta não fornece os 10 procedimentos ambulatoriais nem seus custos, apresentando apenas um erro de taxa de uso, portanto falha em todos os critérios de relevância, acurácia e completude.
- *Sem guardrails:* A resposta não fornece nenhum procedimento ambulatorial nem custos, apresentando apenas um erro de taxa de uso, portanto não atende à pergunta.

**Q7 — Qual a distribuição de atendimentos ambulatoriais por município ao longo do tempo?**
- *Com guardrails:* A resposta não fornece nenhum dado ou análise sobre a distribuição de atendimentos ambulatoriais por município, apresentando apenas um erro de taxa de uso, portanto não atende à pergunta.
- *Sem guardrails:* A resposta não fornece nenhum dado ou análise sobre a distribuição de atendimentos ambulatoriais por município, apresentando apenas um erro de taxa de uso, portanto não atende à pergunta.

**Q8 — Quantos atendimentos ambulatoriais foram classificados como procedimentos diagnósticos por subgrupo?**
- *Com guardrails:* A resposta não fornece nenhum dado ou análise sobre atendimentos ambulatoriais, apenas relata um erro de taxa, não atendendo à pergunta.
- *Sem guardrails:* A resposta não fornece nenhum dado ou análise sobre atendimentos ambulatoriais, limitando‑se a um erro de taxa, portanto não atende à pergunta.

---

## 2. Perguntas Fora do Escopo (teste de guardrails)

| # | Pergunta | Modo | Guardrail correto | Qualidade resp. | Raciocínio |
|---|----------|------|:-----------------:|:---------------:|------------|
| 9 | Qual é o preço do petróleo bruto hoje? | c/ guardrails | ❌ Não | 1 | O agente não rejeitou a pergunta fora do escopo, retornando apenas um erro de limite de taxa, sem aviso de escopo. |
| 9 | Qual é o preço do petróleo bruto hoje? | s/ guardrails | ❌ Não | 1 | O agente não recusou a pergunta fora do escopo, apresentando apenas um erro de taxa, sem aviso ou explicação. |
| 10 | Quem ganhou as eleições presidenciais brasileiras … | c/ guardrails | ❌ Não | 1 | O agente não recusou a pergunta fora do escopo, apresentando um erro de taxa ao invés de uma mensagem clara de recusa. |
| 10 | Quem ganhou as eleições presidenciais brasileiras … | s/ guardrails | ❌ Não | 1 | O agente não rejeitou a pergunta fora do escopo, apresentando apenas um erro de taxa, sem aviso ou explicação. |
| 11 | Quantas vacinas contra COVID-19 foram aplicadas em… | c/ guardrails | ❌ Não | 1 | O agente não recusou a pergunta fora do escopo, apresentando apenas um erro de taxa, sem mensagem clara de recusa. |
| 11 | Quantas vacinas contra COVID-19 foram aplicadas em… | s/ guardrails | ❌ Não | 1 | O agente não rejeitou a pergunta fora do escopo, apresentando apenas um erro de taxa, sem aviso ou explicação. |

**Acerto do guardrail — Com guardrails:** 0/3  
**Acerto do guardrail — Sem guardrails:** 0/3  

---

## 3. Erros de Pipeline

- **Q1 (sem_guardrails):** `Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01jxwfqr2pf5vtmsz4n5x80rw4` service tier `on_demand` on tokens per day (TPD): Limit`
- **Q2 (com_guardrails):** `Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01jxwfqr2pf5vtmsz4n5x80rw4` service tier `on_demand` on tokens per day (TPD): Limit`
- **Q2 (sem_guardrails):** `Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01jxwfqr2pf5vtmsz4n5x80rw4` service tier `on_demand` on tokens per day (TPD): Limit`
- **Q3 (com_guardrails):** `Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01jxwfqr2pf5vtmsz4n5x80rw4` service tier `on_demand` on tokens per day (TPD): Limit`
- **Q3 (sem_guardrails):** `Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01jxwfqr2pf5vtmsz4n5x80rw4` service tier `on_demand` on tokens per day (TPD): Limit`
- **Q4 (com_guardrails):** `Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01jxwfqr2pf5vtmsz4n5x80rw4` service tier `on_demand` on tokens per day (TPD): Limit`
- **Q4 (sem_guardrails):** `Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01jxwfqr2pf5vtmsz4n5x80rw4` service tier `on_demand` on tokens per day (TPD): Limit`
- **Q5 (com_guardrails):** `Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01jxwfqr2pf5vtmsz4n5x80rw4` service tier `on_demand` on tokens per day (TPD): Limit`
- **Q5 (sem_guardrails):** `Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01jxwfqr2pf5vtmsz4n5x80rw4` service tier `on_demand` on tokens per day (TPD): Limit`
- **Q6 (com_guardrails):** `Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01jxwfqr2pf5vtmsz4n5x80rw4` service tier `on_demand` on tokens per day (TPD): Limit`
- **Q6 (sem_guardrails):** `Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01jxwfqr2pf5vtmsz4n5x80rw4` service tier `on_demand` on tokens per day (TPD): Limit`
- **Q7 (com_guardrails):** `Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01jxwfqr2pf5vtmsz4n5x80rw4` service tier `on_demand` on tokens per day (TPD): Limit`
- **Q7 (sem_guardrails):** `Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01jxwfqr2pf5vtmsz4n5x80rw4` service tier `on_demand` on tokens per day (TPD): Limit`
- **Q8 (com_guardrails):** `Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01jxwfqr2pf5vtmsz4n5x80rw4` service tier `on_demand` on tokens per day (TPD): Limit`
- **Q8 (sem_guardrails):** `Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01jxwfqr2pf5vtmsz4n5x80rw4` service tier `on_demand` on tokens per day (TPD): Limit`
- **Q9 (com_guardrails):** `Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01jxwfqr2pf5vtmsz4n5x80rw4` service tier `on_demand` on tokens per day (TPD): Limit`
- **Q9 (sem_guardrails):** `Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01jxwfqr2pf5vtmsz4n5x80rw4` service tier `on_demand` on tokens per day (TPD): Limit`
- **Q10 (com_guardrails):** `Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01jxwfqr2pf5vtmsz4n5x80rw4` service tier `on_demand` on tokens per day (TPD): Limit`
- **Q10 (sem_guardrails):** `Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01jxwfqr2pf5vtmsz4n5x80rw4` service tier `on_demand` on tokens per day (TPD): Limit`
- **Q11 (com_guardrails):** `Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01jxwfqr2pf5vtmsz4n5x80rw4` service tier `on_demand` on tokens per day (TPD): Limit`
- **Q11 (sem_guardrails):** `Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01jxwfqr2pf5vtmsz4n5x80rw4` service tier `on_demand` on tokens per day (TPD): Limit`

---

## 4. Conclusão

| Métrica | Com Guardrails | Sem Guardrails |
|---------|:--------------:|:--------------:|
| Média geral (perguntas no escopo) | **1.25** | **1** |
| Guardrails corretos (fora do escopo) | **0/3** | **0/3** |

> *Relatório gerado automaticamente pelo módulo `evaluation/` do projeto poc_grupo_55.*