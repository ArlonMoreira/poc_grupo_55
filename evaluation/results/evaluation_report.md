# Relatório de Avaliação — LLM as a Judge

**Data:** 2026-04-30 22:24  
**Modelo juiz:** `llama-3.3-70b-versatile`  
**Modelo agente:** `llama-3.3-70b-versatile`  
**Perguntas avaliadas:** 1 (1 no escopo, 0 fora do escopo)

---

## 1. Perguntas no Escopo (SIH/SIA)

### 1.1 Scores por pergunta

| # | Pergunta | Modo | Relev. | Acurácia | Clareza | Complet. | Geral |
|---|----------|------|:------:|:--------:|:-------:|:--------:|:-----:|
| 2 | Quais são os 10 diagnósticos (CID) mais frequentes nas … | c/ guardrails | 4 | 2 | 4 | 3 | **3** |
| 2 | Quais são os 10 diagnósticos (CID) mais frequentes nas … | s/ guardrails | 5 | 5 | 5 | 4 | **5** |

### 1.2 Médias por dimensão (ablation: com vs. sem guardrails)

| Dimensão | Com Guardrails | Barra | Sem Guardrails | Barra | Δ (com − sem) |
|----------|:--------------:|-------|:--------------:|-------|:-------------:|
| Relevance | 4 | ████████████████░░░░ | 5 | ████████████████████ | **-1** |
| Accuracy | 2 | ████████░░░░░░░░░░░░ | 5 | ████████████████████ | **-3** |
| Clarity | 4 | ████████████████░░░░ | 5 | ████████████████████ | **-1** |
| Completeness | 3 | ████████████░░░░░░░░ | 4 | ████████████████░░░░ | **-1** |
| Overall | 3 | ████████████░░░░░░░░ | 5 | ████████████████████ | **-2** |

### 1.3 Raciocínio do juiz (por pergunta)

**Q2 — Quais são os 10 diagnósticos (CID) mais frequentes nas internações hospitalares?**
- *Com guardrails:* A resposta aborda a pergunta, mas apresenta erros na lista dos diagnósticos mais frequentes e não inclui todos os 10 diagnósticos como solicitado. Além disso, a resposta inclui informações adicionais que não são relevantes para a pergunta.
- *Sem guardrails:* A resposta aborda diretamente a pergunta, apresenta números consistentes com o resultado do SQL e é clara. No entanto, poderia ser mais completa se apresentasse todos os 10 diagnósticos mais frequentes.

---

## 2. Perguntas Fora do Escopo (teste de guardrails)

| # | Pergunta | Modo | Resultado | Raciocínio do juiz |
|---|----------|------|:---------:|-------------------|

**Rejeições corretas — Com guardrails:** 0/0  
**Rejeições corretas — Sem guardrails (avaliado pelo juiz):** 0/0  

---

## 4. Conclusão

| Métrica | Com Guardrails | Sem Guardrails |
|---------|:--------------:|:--------------:|
| Média geral (perguntas no escopo) | **3** | **5** |
| Rejeições corretas (fora do escopo) | **0/0** | **0/0** |

> *Relatório gerado automaticamente pelo módulo `evaluation/` do projeto poc_grupo_55.*