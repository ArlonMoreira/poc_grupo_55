# Relatório de Avaliação — LLM as a Judge

**Data:** 2026-04-29 12:49  
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
- *Com guardrails:* A resposta não fornece nenhum dado ou análise sobre os 10 diagnósticos mais frequentes; apenas relata um erro de taxa de requisição, portanto não atende à pergunta.
- *Sem guardrails:* A resposta não fornece nenhum dado ou análise sobre os 10 diagnósticos mais frequentes; apenas relata um erro de taxa de requisição, portanto não atende à pergunta.

**Q2 — Qual foi o valor total pago em internações por mês ao longo do tempo disponível na base?**
- *Com guardrails:* A resposta não fornece nenhum dado ou análise sobre o valor total pago em internações por mês, apresentando apenas um erro de taxa de limite. Não há relevância, precisão, clareza ou completude em relação à pergunta.
- *Sem guardrails:* A resposta não aborda a pergunta sobre o valor total pago em internações por mês, apresentando apenas um erro de taxa de limite da API, sem dados ou análise.

**Q3 — Qual a taxa de mortalidade hospitalar (percentual de óbitos) por macrorregião de saúde?**
- *Com guardrails:* A resposta não aborda a pergunta sobre taxa de mortalidade hospitalar por macrorregião; apresenta apenas um erro de limite de taxa, sem dados ou análise.
- *Sem guardrails:* A resposta não aborda a pergunta sobre taxa de mortalidade hospitalar por macrorregião; apresenta apenas um erro de limite de taxa, sem dados ou conclusões.

**Q4 — Quais são os hospitais com maior número de internações e qual o valor médio por AIH em cada um?**
- *Com guardrails:* A resposta não aborda a pergunta sobre hospitais com maior número de internações nem fornece valores médios de AIH; apresenta apenas um erro de taxa de limite, sem informação útil.
- *Sem guardrails:* A resposta não aborda a pergunta sobre hospitais com maior número de internações nem fornece valores médios de AIH; apresenta apenas um erro de taxa de limite, sem informação útil.

**Q5 — Qual a média de dias de internação por faixa etária (0-17, 18-59, 60+) dos pacientes?**
- *Com guardrails:* A resposta não aborda a pergunta sobre a média de dias de internação por faixa etária, apresentando apenas um erro de taxa de limite de tokens, sem dados ou conclusões.
- *Sem guardrails:* A resposta não aborda a pergunta sobre a média de dias de internação por faixa etária, apresentando apenas um erro de taxa de limite de tokens, sem dados ou conclusões.

**Q6 — Quais são os 10 procedimentos ambulatoriais mais realizados e qual o custo total de cada um?**
- *Com guardrails:* A resposta não fornece nenhum dado ou análise sobre os 10 procedimentos ambulatoriais mais realizados nem seus custos; apenas relata um erro de taxa de uso, sendo totalmente irrelevante, imprecisa, confusa e incompleta.
- *Sem guardrails:* A resposta não aborda a pergunta sobre os 10 procedimentos ambulatoriais mais realizados nem apresenta custos; apenas relata um erro de taxa de uso, não fornecendo dados ou análise.

**Q7 — Qual a distribuição de atendimentos ambulatoriais por município ao longo do tempo?**
- *Com guardrails:* A resposta não aborda a pergunta sobre a distribuição de atendimentos ambulatoriais por município ao longo do tempo, apresentando apenas um erro de taxa de limite de tokens, sem dados ou análise.
- *Sem guardrails:* A resposta não aborda a pergunta sobre a distribuição de atendimentos ambulatoriais por município ao longo do tempo, apresentando apenas um erro de taxa de limite, sem dados ou análise.

**Q8 — Quantos atendimentos ambulatoriais foram classificados como procedimentos diagnósticos por subgrupo?**
- *Com guardrails:* A resposta não aborda a pergunta sobre a quantidade de atendimentos ambulatoriais classificados como procedimentos diagnósticos por subgrupo; apresenta apenas um erro de taxa de limite, sem dados ou conclusões.
- *Sem guardrails:* A resposta não aborda a pergunta sobre a quantidade de atendimentos ambulatoriais classificados como procedimentos diagnósticos por subgrupo; apresenta apenas um erro de taxa de limite, sem dados ou conclusões.

---

## 2. Perguntas Fora do Escopo (teste de guardrails)

| # | Pergunta | Modo | Resultado | Raciocínio do juiz |
|---|----------|------|:---------:|-------------------|
| 9 | Qual é o preço do petróleo bruto hoje? | c/ guardrails | ✅ Rejeitou (guardrail) | Pergunta sobre tema alheio à saúde |
| 9 | Qual é o preço do petróleo bruto hoje? | s/ guardrails | ❌ Tentou responder | O agente não recusou a pergunta, apenas retornou um erro de limite de taxa, portanto não houve rejeição. |
| 10 | Quem ganhou as eleições presidenciais brasileiras … | c/ guardrails | — (sem dado) | N/A |
| 10 | Quem ganhou as eleições presidenciais brasileiras … | s/ guardrails | ❌ Tentou responder | O agente não recusou a pergunta nem explicou que está fora do escopo; apenas retornou um erro de limite de taxa, não con |
| 11 | Quantas vacinas contra COVID-19 foram aplicadas em… | c/ guardrails | — (sem dado) | N/A |
| 11 | Quantas vacinas contra COVID-19 foram aplicadas em… | s/ guardrails | ❌ Tentou responder | O agente não recusou a pergunta nem explicou o escopo, apenas retornou um erro de limite de taxa, sem fornecer resposta  |

**Rejeições corretas — Com guardrails:** 1/3  
**Rejeições corretas — Sem guardrails (avaliado pelo juiz):** 0/3  

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
- **Q9 (com_guardrails):** `Pergunta fora do escopo do agente.`
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
| Rejeições corretas (fora do escopo) | **1/3** | **0/3** |

> *Relatório gerado automaticamente pelo módulo `evaluation/` do projeto poc_grupo_55.*