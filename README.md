# Agente Inteligente SIH/SUS — Grupo 55

Prova de conceito de um agente conversacional que responde perguntas em linguagem natural sobre internações hospitalares do SIH/SUS (DATASUS / Goiás), consultando um banco de dados PostgreSQL via SQL gerado por LLM.

---

## Arquitetura do Agente

O agente executa um pipeline de 6 etapas para cada pergunta:

```
Pergunta → Planner → SQL Builder → Executor → Analista → Verificador → Comunicador → Resposta
```

| Etapa | Responsabilidade |
|---|---|
| **Planner / Router** | Interpreta a pergunta e define a estratégia de consulta |
| **SQL Builder** | Gera a query PostgreSQL (com retry automático em caso de erro) |
| **Executor** | Executa a query no banco de dados |
| **Data Analyst** | Análise descritiva dos resultados retornados |
| **Verifier** | Checagem de consistência e guardrails |
| **Communicator** | Gera a resposta final em linguagem acessível |

---

## Requisitos

- Python 3.8+
- PostgreSQL 12+
- Docker (para subir o banco localmente)
- Chave de API Groq (`GROQ_API_KEY`)
- Arquivo `internacoes.csv` — [baixar no Google Drive](https://drive.google.com/file/d/1AzUo9ebia-PJRjH-M2nlo40umnCohZry/view?usp=sharing)

---

## 1. Clonar o Repositório

```bash
git clone git@github.com:ArlonMoreira/poc_grupo_55.git
cd poc_grupo_55
```

> **Nota:** Certifique-se de que a chave SSH está configurada no GitHub. Consulte a [documentação do GitHub](https://docs.github.com/en/authentication/connecting-to-github-with-ssh) se necessário.

---

## 2. Carregar os Dados no PostgreSQL

### 2.1 Baixar o CSV

Baixe o arquivo `internacoes.csv` e coloque na raiz do projeto (`poc_grupo_55/`).

### 2.2 Configurar e executar o script de carga

```bash
cd carga/
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python load_csv_postgress_auto.py
```

> **Nota:** Esse ambiente virtual é específico para a carga e separado do ambiente do agente.

---

## 3. Configurar o Agente

### 3.1 Criar o arquivo `.env`

Copie o exemplo e preencha com suas credenciais:

```bash
cp .env.example .env
```

Variáveis necessárias:

```env
# Banco de dados
DB_HOST=localhost
DB_PORT=5432
DB_USER=datasus
DB_PASSWORD=datasus
DB_NAME=datasus

# Groq
GROQ_API_KEY=sua_chave_aqui
GROQ_MODEL=llama-3.3-70b-versatile   # opcional, este é o padrão
```

### 3.2 Criar o ambiente virtual do agente

Na raiz do projeto:

```bash
python -m venv agent_venv
source agent_venv/bin/activate
pip install -r requirements_agent.txt
```

---

## 4. Executar o Agente

### Modo interativo

```bash
python main.py
```

### Pergunta direta via argumento

```bash
python main.py "Qual o diagnóstico mais comum nas internações em 2023?"
```

---

## Estrutura do Projeto

```
poc_grupo_55/
├── agent/
│   ├── config.py        # Configurações e variáveis de ambiente
│   ├── pipeline.py      # Orquestração das 6 etapas
│   ├── steps.py         # Implementação de cada etapa (LLM calls)
│   └── tools.py         # Ferramentas (execução SQL)
├── carga/
│   ├── load_csv_postgress_auto.py   # Script de carga principal
│   └── requirements.txt
├── docs/
│   └── about_data.md    # Schema e descrição dos dados
├── main.py              # Entrypoint do agente
├── requirements_agent.txt
└── .env.example
```
