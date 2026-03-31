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

- [Docker](https://docs.docker.com/get-docker/) e [Docker Compose](https://docs.docker.com/compose/)
- [VS Code](https://code.visualstudio.com/) com a extensão [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
- Chave de API Groq (`GROQ_API_KEY`)
- Arquivo `internacoes.csv` — [baixar no Google Drive](https://drive.google.com/file/d/1AzUo9ebia-PJRjH-M2nlo40umnCohZry/view?usp=sharing)

---

## 1. Clonar o Repositório

```bash
git clone git@github.com:ArlonMoreira/poc_grupo_55.git
cd poc_grupo_55
```

---

## 2. Configurar o `.env`

```bash
cp .env.example .env
```

Edite o `.env` e preencha sua chave Groq:

```env
GROQ_API_KEY=sua_chave_aqui
GROQ_MODEL=llama-3.3-70b-versatile   # opcional, este é o padrão

DB_HOST=postgres   # nome do serviço no docker-compose
DB_PORT=5432
DB_USER=datasus
DB_PASSWORD=datasus
DB_NAME=datasus
```

---

## 3. Abrir no Dev Container

1. Coloque o arquivo `internacoes.csv` na raiz do projeto.
2. Abra o projeto no VS Code.
3. Quando solicitado, clique em **"Reopen in Container"** — ou use o comando `Dev Containers: Reopen in Container` na paleta de comandos (`Ctrl+Shift+P`).

O VS Code irá:
- Construir a imagem do agente (`Dockerfile`)
- Subir o PostgreSQL via Docker Compose
- Abrir o terminal já dentro do container
- Se o container falhar, verifique se a porta do PostgresSQL já esta sendo usada, em caso afirmativo, faça: `sudo systemctl stop postgresql`


---

## 4. Carregar os Dados

Com o container aberto, execute no terminal integrado:

```bash
python carga/load_csv_postgress_auto.py
```

> Isso só precisa ser feito uma vez. Os dados ficam persistidos no volume `postgres_data`.

---

## 5. Executar o Agente

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
├── .devcontainer/
│   └── devcontainer.json    # Configuração do Dev Container
├── agent/
│   ├── config.py            # Configurações e variáveis de ambiente
│   ├── pipeline.py          # Orquestração das 6 etapas
│   ├── steps.py             # Implementação de cada etapa (LLM calls)
│   └── tools.py             # Ferramentas (execução SQL)
├── carga/
│   └── load_csv_postgress_auto.py   # Script de carga do CSV
├── docs/
│   └── about_data.md        # Schema e descrição dos dados
├── docker-compose.yml       # Serviços: postgres + agent
├── Dockerfile               # Imagem do agente
├── main.py                  # Entrypoint do agente
├── requirements.txt         # Dependências de carga
├── requirements_agent.txt   # Dependências do agente
└── .env.example
```
