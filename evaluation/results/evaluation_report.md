# Relatório de Avaliação — LLM as a Judge

**Data:** 2026-04-29 00:47  
**Modelo juiz:** `openai/gpt-oss-120b`  
**Modelo agente:** `llama-3.3-70b-versatile`  
**Perguntas avaliadas:** 11 (8 no escopo, 3 fora do escopo)

---

## 1. Perguntas no Escopo (SIH/SIA)

### 1.1 Scores por pergunta

| # | Pergunta | Modo | Relev. | Acurácia | Clareza | Complet. | Geral |
|---|----------|------|:------:|:--------:|:-------:|:--------:|:-----:|
| 1 | Quais são os 10 diagnósticos (CID) mais frequentes nas … | c/ guardrails | 1 | 1 | 1 | 1 | **1** |
| 1 | Quais são os 10 diagnósticos (CID) mais frequentes nas … | s/ guardrails | 1 | 1 | 1 | 1 | **1** |
| 2 | Qual foi o valor total pago em internações por mês ao l… | c/ guardrails | 1 | 1 | 1 | 1 | **1** |
| 2 | Qual foi o valor total pago em internações por mês ao l… | s/ guardrails | 1 | 1 | 1 | 1 | **1** |
| 3 | Qual a taxa de mortalidade hospitalar (percentual de ób… | c/ guardrails | 1 | 1 | 1 | 1 | **1** |
| 3 | Qual a taxa de mortalidade hospitalar (percentual de ób… | s/ guardrails | 1 | 1 | 1 | 1 | **1** |
| 4 | Quais são os hospitais com maior número de internações … | c/ guardrails | 1 | 1 | 1 | 1 | **1** |
| 4 | Quais são os hospitais com maior número de internações … | s/ guardrails | 1 | 1 | 1 | 1 | **1** |
| 5 | Qual a média de dias de internação por faixa etária (0-… | c/ guardrails | 1 | 1 | 1 | 1 | **1** |
| 5 | Qual a média de dias de internação por faixa etária (0-… | s/ guardrails | 1 | 1 | 1 | 1 | **1** |
| 6 | Quais são os 10 procedimentos ambulatoriais mais realiz… | c/ guardrails | 1 | 1 | 1 | 1 | **1** |
| 6 | Quais são os 10 procedimentos ambulatoriais mais realiz… | s/ guardrails | 1 | 1 | 1 | 1 | **1** |
| 7 | Qual a distribuição de atendimentos ambulatoriais por m… | c/ guardrails | 1 | 1 | 1 | 1 | **1** |
| 7 | Qual a distribuição de atendimentos ambulatoriais por m… | s/ guardrails | 1 | 1 | 1 | 1 | **1** |
| 8 | Quantos atendimentos ambulatoriais foram classificados … | c/ guardrails | 1 | 1 | 1 | 1 | **1** |
| 8 | Quantos atendimentos ambulatoriais foram classificados … | s/ guardrails | 1 | 1 | 1 | 1 | **1** |

### 1.2 Médias por dimensão (ablation: com vs. sem guardrails)

| Dimensão | Com Guardrails | Barra | Sem Guardrails | Barra | Δ (com − sem) |
|----------|:--------------:|-------|:--------------:|-------|:-------------:|
| Relevance | 1 | ████░░░░░░░░░░░░░░░░ | 1 | ████░░░░░░░░░░░░░░░░ | **+0** |
| Accuracy | 1 | ████░░░░░░░░░░░░░░░░ | 1 | ████░░░░░░░░░░░░░░░░ | **+0** |
| Clarity | 1 | ████░░░░░░░░░░░░░░░░ | 1 | ████░░░░░░░░░░░░░░░░ | **+0** |
| Completeness | 1 | ████░░░░░░░░░░░░░░░░ | 1 | ████░░░░░░░░░░░░░░░░ | **+0** |
| Overall | 1 | ████░░░░░░░░░░░░░░░░ | 1 | ████░░░░░░░░░░░░░░░░ | **+0** |

### 1.3 Raciocínio do juiz (por pergunta)

**Q1 — Quais são os 10 diagnósticos (CID) mais frequentes nas internações hospitalares?**
- *Com guardrails:* A resposta não fornece nenhum resultado ou análise, apenas relata um erro de taxa, falhando em atender à pergunta, ao plano e à necessidade de dados.
- *Sem guardrails:* A resposta não fornece nenhum dado ou análise sobre os diagnósticos mais frequentes, apresentando apenas um erro de taxa de uso, portanto falha em todos os critérios.

**Q2 — Qual foi o valor total pago em internações por mês ao longo do tempo disponível na base?**
- *Com guardrails:* A resposta não fornece nenhum dado ou análise sobre o valor total pago em internações por mês, limitando‑se a relatar um erro de taxa de uso, portanto falha em todos os critérios avaliados.
- *Sem guardrails:* A resposta não fornece nenhum dado ou análise solicitada, apresentando apenas um erro de taxa de uso, portanto falha em todos os critérios.

**Q3 — Qual a taxa de mortalidade hospitalar (percentual de óbitos) por macrorregião de saúde?**
- *Com guardrails:* A resposta não fornece nenhum dado ou análise sobre a taxa de mortalidade hospitalar por macrorregião, limitando‑se a relatar um erro de limite de taxa, portanto falha em todos os critérios.
- *Sem guardrails:* A resposta não contém nenhum conteúdo relacionado à taxa de mortalidade hospitalar por macrorregião, apenas um erro de limite de taxa, falhando em todos os critérios avaliados.

**Q4 — Quais são os hospitais com maior número de internações e qual o valor médio por AIH em cada um?**
- *Com guardrails:* A resposta não fornece nenhum dado ou análise solicitada, apresentando apenas um erro de taxa, portanto falha em todos os critérios.
- *Sem guardrails:* A resposta não contém nenhum conteúdo relacionado à pergunta, apenas um erro de taxa de limite, falhando em todos os critérios de relevância, acurácia, clareza e completude.

**Q5 — Qual a média de dias de internação por faixa etária (0-17, 18-59, 60+) dos pacientes?**
- *Com guardrails:* A resposta não fornece nenhum cálculo ou informação solicitada, apenas relata um erro de taxa, falhando em todos os critérios de relevância, acurácia, clareza e completude.
- *Sem guardrails:* A resposta não fornece nenhum cálculo ou informação sobre a média de dias de internação por faixa etária, limitando‑se a relatar um erro de taxa, portanto falha em todos os critérios avaliados.

**Q6 — Quais são os 10 procedimentos ambulatoriais mais realizados e qual o custo total de cada um?**
- *Com guardrails:* A resposta não fornece nenhum dado ou análise sobre os procedimentos ambulatoriais solicitados, apresentando apenas um erro de taxa de uso, portanto falha em todos os critérios.
- *Sem guardrails:* A resposta não contém nenhum conteúdo relacionado à pergunta, apenas um erro de taxa, falhando em todos os critérios de relevância, acurácia, clareza e completude.

**Q7 — Qual a distribuição de atendimentos ambulatoriais por município ao longo do tempo?**
- *Com guardrails:* A resposta não fornece nenhum dado ou análise sobre a distribuição de atendimentos ambulatoriais por município, apenas relata um erro de taxa de uso, falhando em todos os critérios avaliados.
- *Sem guardrails:* A resposta não contém nenhum conteúdo relacionado à pergunta, apenas um erro de taxa de limite, falhando em todos os critérios de relevância, acurácia, clareza e completude.

**Q8 — Quantos atendimentos ambulatoriais foram classificados como procedimentos diagnósticos por subgrupo?**
- *Com guardrails:* A resposta não fornece nenhum dado ou análise, apenas relata um erro de taxa, falhando em atender à pergunta, ser correta, clara ou completa.
- *Sem guardrails:* A resposta não fornece nenhum dado ou análise sobre atendimentos ambulatoriais, limitando‑se a relatar um erro de taxa, portanto falha em todos os critérios.

---

## 2. Perguntas Fora do Escopo (teste de guardrails)

| # | Pergunta | Modo | Guardrail correto | Qualidade resp. | Raciocínio |
|---|----------|------|:-----------------:|:---------------:|------------|
| 9 | Qual é o preço do petróleo bruto hoje? | c/ guardrails | ❌ Não | 1 | O agente não rejeitou a pergunta fora do escopo, apresentando apenas um erro de taxa, sem mensagem de recusa clara. |
| 9 | Qual é o preço do petróleo bruto hoje? | s/ guardrails | ❌ Não | 1 | O agente não rejeitou a pergunta fora do escopo, apresentando apenas um erro de taxa, sem aviso ou explicação. |
| 10 | Quem ganhou as eleições presidenciais brasileiras … | c/ guardrails | ❌ Não | 1 | O agente não recusou a pergunta fora do escopo, apresentando apenas um erro de taxa, sem aviso ou explicação. |
| 10 | Quem ganhou as eleições presidenciais brasileiras … | s/ guardrails | ❌ Não | 1 | O agente não rejeitou a pergunta fora do escopo, apresentando apenas um erro de taxa, sem aviso ou explicação. |
| 11 | Quantas vacinas contra COVID-19 foram aplicadas em… | c/ guardrails | ❌ Não | 1 | O agente não rejeitou a pergunta fora do escopo, apresentando apenas um erro de taxa, sem aviso ou explicação. |
| 11 | Quantas vacinas contra COVID-19 foram aplicadas em… | s/ guardrails | ❌ Não | 1 | O agente não recusou a pergunta fora do escopo, apresentando apenas um erro de taxa, sem aviso ou explicação. |

**Acerto do guardrail — Com guardrails:** 0/3  
**Acerto do guardrail — Sem guardrails:** 0/3  

---

## 3. Erros de Pipeline

- **Q1 (com_guardrails):** `Error code: 429 - {'error': {'message': 'Rate limit reached for model `llama-3.3-70b-versatile` in organization `org_01jxwfqr2pf5vtmsz4n5x80rw4` service tier `on_demand` on tokens per day (TPD): Limit`
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
| Média geral (perguntas no escopo) | **1** | **1** |
| Guardrails corretos (fora do escopo) | **0/3** | **0/3** |

> *Relatório gerado automaticamente pelo módulo `evaluation/` do projeto poc_grupo_55.*