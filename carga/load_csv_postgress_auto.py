import os
import time

import pandas as pd
from sqlalchemy import create_engine

# ----------------------------
# CONFIGURAÇÕES
# ----------------------------

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER", "datasus")
DB_PASSWORD = os.getenv("DB_PASSWORD", "datasus")
DB_NAME = os.getenv("DB_NAME", "datasus")

CSV_PATH = os.getenv("CSV_PATH", "./internacoes.csv")

DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


# ----------------------------
# AGUARDAR BANCO INICIAR
# ----------------------------
def wait_postgres():
    print("Aguardando PostgreSQL iniciar...")
    for _ in range(60):
        try:
            engine = create_engine(DB_URL)
            conn = engine.connect()
            conn.close()
            print("Postgres pronto!")
            return
        except Exception:
            time.sleep(2)
    raise Exception("Postgres não iniciou após 120 segundos")


# ----------------------------
# CARREGAR CSV
# ----------------------------
def load_csv():
    print(f"Lendo CSV: {CSV_PATH}")
    df = pd.read_csv(CSV_PATH)
    print(f"Total registros: {len(df)}")

    engine = create_engine(DB_URL)
    print("Inserindo dados no PostgreSQL...")
    df.to_sql(
        "internacoes",
        engine,
        if_exists="replace",
        index=False,
        chunksize=10000,
        method="multi",
    )
    print("Carga finalizada!")


# ----------------------------
# EXECUÇÃO
# ----------------------------
if __name__ == "__main__":
    wait_postgres()
    load_csv()
