# Etapa de Carregamento dos Dados

## Requisitos

- Python 3.8+
- PostgreSQL 12+
- Git com SSH configurado
- pip e venv (geralmente inclusos com Python)
- Arquivo `internacoes.csv` baixado do Google Drive
- Dependências Python listadas em `requirements.txt` (pandas, psycopg2, python-dotenv ou similares para conexão com banco de dados)
- Docker presente no ambiente

## 1. Clonar o Repositório

Clone o projeto em seu ambiente local:

```bash
git clone git@github.com:ArlonMoreira/poc_grupo_55.git
```

> **Nota:** Certifique-se de que a chave SSH está configurada no GitHub. Consulte a [documentação do GitHub](https://docs.github.com/en/authentication/connecting-to-github-with-ssh) se necessário.

## 2. Baixar os Dados

Baixe o arquivo `internacoes.csv` em [Google Drive](https://drive.google.com/file/d/1AzUo9ebia-PJRjH-M2nlo40umnCohZry/view?usp=sharing) e coloque na raiz do projeto `poc_grupo_55/`.

## 3. Acessar a Pasta de Carregamento

Navegue até a pasta `cargas`:

```bash
cd poc_grupo_55/cargas/
```

> **Nota:** O script deve ser executado de dentro desta pasta.

## 4. Configurar o Ambiente Virtual Python

Execute os comandos em sequência:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
> **Nota:** Esse ambiente virtual é específico para a carga.

## 5. Executar o Script de Carregamento

```bash
python load_csv_postgress_auto.py
```