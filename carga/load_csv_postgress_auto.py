import subprocess
import time
import pandas as pd
from sqlalchemy import create_engine

# ----------------------------
# CONFIGURAÇÕES
# ----------------------------

CONTAINER_NAME = "postgres_datasus"

POSTGRES_USER = "datasus"
POSTGRES_PASSWORD = "datasus"
POSTGRES_DB = "datasus"

POSTGRES_PORT = "5432"

CSV_PATH = "../internacoes.csv"

DB_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:{POSTGRES_PORT}/{POSTGRES_DB}"


# ----------------------------
# VERIFICAR SE CONTAINER EXISTE
# ----------------------------
def container_exists():

    result = subprocess.run(
        ["docker", "ps", "-a", "--format", "{{.Names}}"],
        capture_output=True,
        text=True
    )

    return CONTAINER_NAME in result.stdout


# ----------------------------
# VERIFICAR SE CONTAINER ESTÁ RODANDO
# ----------------------------
def container_running():

    result = subprocess.run(
        ["docker", "ps", "--format", "{{.Names}}"],
        capture_output=True,
        text=True
    )

    return CONTAINER_NAME in result.stdout


# ----------------------------
# SUBIR POSTGRES
# ----------------------------
def start_postgres():

    if not container_exists():

        print("Criando container postgres...")

        subprocess.run([
            "docker", "run", "-d",
            "--name", CONTAINER_NAME,
            "-e", f"POSTGRES_USER={POSTGRES_USER}",
            "-e", f"POSTGRES_PASSWORD={POSTGRES_PASSWORD}",
            "-e", f"POSTGRES_DB={POSTGRES_DB}",
            "-p", f"{POSTGRES_PORT}:5432",
            "postgres:16"
        ])

    elif not container_running():

        print("Iniciando container postgres existente...")

        subprocess.run(["docker", "start", CONTAINER_NAME])

    else:

        print("Postgres já está rodando")


# ----------------------------
# AGUARDAR BANCO INICIAR
# ----------------------------
def wait_postgres():

    print("Aguardando PostgreSQL iniciar...")

    for i in range(60):

        try:

            engine = create_engine(DB_URL)

            conn = engine.connect()
            conn.close()

            print("Postgres pronto!")
            return

        except Exception:

            time.sleep(2)

    raise Exception("Postgres não iniciou")


# ----------------------------
# CARREGAR CSV
# ----------------------------
def load_csv():

    print("Lendo CSV...")

    df = pd.read_csv(CSV_PATH)

    print("Total registros:", len(df))

    engine = create_engine(DB_URL)

    print("Inserindo dados no PostgreSQL...")

    df.to_sql(
        "internacoes",
        engine,
        if_exists="replace",
        index=False,
        chunksize=10000,
        method="multi"
    )

    print("Carga finalizada!")


# ----------------------------
# EXECUÇÃO
# ----------------------------
if __name__ == "__main__":

    start_postgres()

    wait_postgres()

    load_csv()