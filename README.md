# Agente Inteligente SIH/SIA/SUS — Grupo 55

Prova de conceito de um agente conversacional que responde perguntas em linguagem natural sobre **internações hospitalares** (SIH/SUS) e **atendimentos ambulatoriais** (SIA/SUS) do DATASUS/Goiás, consultando um banco de dados PostgreSQL via SQL gerado por LLM.

---

## Arquitetura do Agente

O agente executa um pipeline de 6 etapas para cada pergunta:

```
Pergunta → Planner → SQL Builder → Executor → Analista → Verificador → Comunicador → Resposta
```

| Etapa | Responsabilidade |
|---|---|
| **Planner / Router** | Interpreta a pergunta, decide qual(is) tabela(s) consultar e define a estratégia de análise |
| **SQL Builder** | Gera a query PostgreSQL (com retry automático em caso de erro) |
| **Executor** | Executa a query no banco de dados |
| **Data Analyst** | Análise descritiva dos resultados retornados |
| **Verifier** | Checagem de consistência e guardrails |
| **Communicator** | Gera a resposta final em linguagem acessível |

### Tabelas disponíveis

| Tabela | Fonte | Unidade de análise |
|---|---|---|
| `public.internacoes` | SIH/SUS | Uma linha = uma AIH (internação hospitalar) |
| `public.atendimentos_ambulatorial` | SIA/SUS | Uma linha = um atendimento/procedimento ambulatorial |

---

## Requisitos

- [Docker](https://docs.docker.com/get-docker/) e [Docker Compose](https://docs.docker.com/compose/)
- [VS Code](https://code.visualstudio.com/) com a extensão [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
- Chave de API Groq (`GROQ_API_KEY`)

> Os arquivos de dados são baixados automaticamente do Google Drive durante a etapa de carga — não é necessário baixar nada manualmente.

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

1. Abra o projeto no VS Code.
2. Quando solicitado, clique em **"Reopen in Container"** — ou use o comando `Dev Containers: Reopen in Container` na paleta de comandos (`Ctrl+Shift+P`).

O VS Code irá:
- Construir a imagem do agente (`Dockerfile`)
- Subir o PostgreSQL via Docker Compose
- Abrir o terminal já dentro do container

> Se o container falhar, verifique se a porta do PostgreSQL já está sendo usada. Em caso afirmativo: `sudo systemctl stop postgresql`

---

## 4. Carregar os Dados

Dentro do terminal do container, execute o script de carga:

```bash
python carga/load_csv_postgress_auto.py
```

O script irá automaticamente:
- Baixar `internacoes.csv` e `ambulatorial.csv` do Google Drive
- Carregar cada arquivo nas respectivas tabelas do PostgreSQL (`internacoes` e `atendimentos_ambulatorial`)
- Remover os arquivos CSV após a carga

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
python main.py "Quais os procedimentos ambulatoriais mais realizados em Goiânia?"
```

---

## Estrutura do Projeto

```
poc_grupo_55/
├── .devcontainer/
│   └── devcontainer.json              # Configuração do Dev Container
├── agent/
│   ├── config.py                      # Configurações e variáveis de ambiente
│   ├── pipeline.py                    # Orquestração das 6 etapas
│   ├── steps.py                       # Implementação de cada etapa (LLM calls)
│   └── tools.py                       # Ferramentas (execução SQL, visualização)
├── carga/
│   ├── load_csv_postgress_auto.py     # Baixa os CSVs do Drive e carrega no PostgreSQL
│   ├── carga_dremio_para_csv.py       # Gera os CSVs a partir do Dremio (uso interno)
│   └── requirements.txt              # Dependências do script de carga
├── docs/
│   └── about_data.md                  # Schema e descrição das tabelas
├── docker-compose.yml                 # Serviços: postgres + agent
├── Dockerfile                         # Imagem do agente
├── main.py                            # Entrypoint do agente
├── requirements_agent.txt             # Dependências do agente
└── .env.example
```
