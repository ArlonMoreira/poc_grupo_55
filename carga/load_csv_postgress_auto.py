import os
import time

import pandas as pd
from sqlalchemy import create_engine
import gdown

# ----------------------------
# CONFIGURAÇÕES
# ----------------------------

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER", "datasus")
DB_PASSWORD = os.getenv("DB_PASSWORD", "datasus")
DB_NAME = os.getenv("DB_NAME", "datasus")

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
# BAIXAR ARQUIVOS DO GOOGLE DRIVE
# ----------------------------
def download_csv_from_drive(file_id, output_path):
    """Baixa arquivo do Google Drive usando gdown"""
    print(f"Baixando arquivo do Google Drive: {file_id}")
    url = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(url, output_path, quiet=False)
    print(f"Arquivo baixado com sucesso: {output_path}")


# ----------------------------
# CARREGAR CSV
# ----------------------------
def load_csv(csv_path, table_name):
    print(f"Lendo CSV: {csv_path}")
    df = pd.read_csv(csv_path, dtype={"PROCEDIMENTO_CODIGO": str})
    print(f"Total registros: {len(df)}")

    engine = create_engine(DB_URL)
    print(f"Inserindo dados na tabela '{table_name}' no PostgreSQL...")
    df.to_sql(
        table_name,
        engine,
        if_exists="replace",
        index=False,
        chunksize=10000,
        method="multi",
    )
    print(f"Carga da tabela '{table_name}' finalizada!")

    # Deletar arquivo CSV após carga
    if os.path.exists(csv_path):
        os.remove(csv_path)
        print(f"Arquivo CSV '{csv_path}' removido após carga.")


# ----------------------------
# CARREGAR AMBOS OS CSVs
# ----------------------------
def load_both_csvs():
    # URLs do Google Drive
    DRIVE_FILES = {
        "internacoes": {
            "file_id": "1z0P62f8yX0Xbp6mYNcXvscEZFABveidu",
            "output_path": "../internacoes.csv"
        },
        "ambulatorial": {
            "file_id": "1N0PANWM7sAsok27dlrTbpF8CC7EajXpu",
            "output_path": "../ambulatorial.csv"
        }
    }

    # Baixar e carregar internações
    print("\n" + "="*50)
    print("BAIXANDO E CARREGANDO INTERNAÇÕES")
    print("="*50)
    download_csv_from_drive(
        DRIVE_FILES["internacoes"]["file_id"],
        DRIVE_FILES["internacoes"]["output_path"]
    )
    load_csv(DRIVE_FILES["internacoes"]["output_path"], "internacoes")

    # Baixar e carregar ambulatorial
    print("\n" + "="*50)
    print("BAIXANDO E CARREGANDO AMBULATORIAL")
    print("="*50)
    download_csv_from_drive(
        DRIVE_FILES["ambulatorial"]["file_id"],
        DRIVE_FILES["ambulatorial"]["output_path"]
    )
    load_csv(DRIVE_FILES["ambulatorial"]["output_path"], "atendimentos_ambulatorial")


# ----------------------------
# EXECUÇÃO
# ----------------------------
if __name__ == "__main__":
    wait_postgres()
    load_both_csvs()
