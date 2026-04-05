import os
import pyodbc
import pandas as pd

# ----------------------------
# CONFIG DREMIO
# ----------------------------
DREMIO_CONFIG = {
    "USER": os.getenv("DREMIO_USER"),
    "PASSWORD": os.getenv("DREMIO_PASSWORD"),
    "HOST": os.getenv("DREMIO_HOST"),
    "PORT": int(os.getenv("DREMIO_PORT", 31010)),
    "DRIVER": os.getenv(
        "DREMIO_DRIVER",
        "/opt/dremio-odbc/lib64/libdrillodbc_sb64.so"
    ),
}

SQL_INTERNACOES = """
SELECT
    distinct
    N_AIH,
    dmun.dmun_municipio AS PACIENTE_RESIDENCIA_MUNICIPIO,
    dmun.dmun_regiao AS PACIENTE_RESIDENCIA_REGIAO,
    dmun.dmun_macro_regiao AS PACIENTE_RESIDENCIA_MACRORREGIAO,
    dmun.dmun_uf_nomex AS PACIENTE_RESIDENCIA_ESTADO,
    IDADE PACIENTE_IDADE,
    MORTE PACIENTE_OBITO,
    CAST(sigtap.dsig_ipcod AS VARCHAR) AS PROCEDIMENTO_CODIGO,
    sigtap.dsig_ipdscr AS PROCEDIMENTO_DESCRICAO,
    TO_DATE(CAST(DT_INTER AS VARCHAR), 'yyyyMMdd') AS DATA_INTERNACAO,
    TO_DATE(CAST(DT_SAIDA AS VARCHAR), 'yyyyMMdd') AS DATA_SAIDA,
    cid.dcid_cid10_codigo CID_CODIGO,
    CASE
        WHEN cid.dcid_cid10_subcategoria = '-' THEN cid.dcid_cid10_categoria
        ELSE cid.dcid_cid10_subcategoria
    END AS CID_DESCRICAO,
    des.desa_cnes UNIDADE_SAUDE_CNES,
    des.desa_nome_fanta UNIDADE_SAUDE_NOME_FANTA,
    dmundes.dmun_municipio AS UNIDADE_SAUDE_MUNICIPIO,
    dmundes.dmun_regiao AS UNIDADE_SAUDE_REGIAO,
    dmundes.dmun_macro_regiao AS UNIDADE_SAUDE_MACRORREGIAO,
    dmundes.dmun_uf_nomex AS UNIDADE_SAUDE_ESTADO,
    rd.QT_DIARIAS,
    rd.VAL_TOT
FROM datalake.refined.sih.rd rd
INNER JOIN "MariaDB Prod".dimensao.d_municipio dmun
    ON dmun.dmun_codibge = rd.MUNIC_RES
INNER JOIN "MariaDB Prod".dimensao.d_sigtap sigtap
    ON sigtap.dsig_ipcod = rd.PROC_SOLIC
INNER JOIN "MariaDB Prod".dimensao.d_cid10 cid
    ON cid.dcid_cid10_codigo = DIAG_PRINC
INNER JOIN "MariaDB Prod".dimensao.d_estabelecimento_saude des
    ON des.desa_cnes = CNES
INNER JOIN "MariaDB Prod".dimensao.d_municipio dmundes
    ON dmundes.dmun_codibge = des.desa_ibge
WHERE rd.DT_INTER BETWEEN 20220101 AND 20251231
limit 500000
"""

SQL_AMBULATORIAL = """
SELECT
    DISTINCT
    dmun.dmun_municipio AS PACIENTE_RESIDENCIA_MUNICIPIO,
    dmun.dmun_regiao AS PACIENTE_RESIDENCIA_REGIAO,
    dmun.dmun_macro_regiao AS PACIENTE_RESIDENCIA_MACRORREGIAO,
    dmun.dmun_uf_nomex AS PACIENTE_RESIDENCIA_ESTADO,
    cast(PA_IDADE as int) AS PACIENTE_IDADE,
    PA_OBITO AS PACIENTE_OBITO,
    CAST(sigtap.dsig_ipcod AS VARCHAR) AS PROCEDIMENTO_CODIGO,
    sigtap.dsig_ipdscr AS PROCEDIMENTO_DESCRICAO,
    TO_DATE(CAST(PA_CMP AS VARCHAR), 'yyyyMM') AS PERIODO_PROCEDIMENTO,
    cid.dcid_cid10_codigo CID_CODIGO,
    CASE
        WHEN cid.dcid_cid10_subcategoria = '-' THEN cid.dcid_cid10_categoria
        ELSE cid.dcid_cid10_subcategoria
    END AS CID_DESCRICAO,
    des.desa_cnes UNIDADE_SAUDE_CNES,
    des.desa_nome_fanta UNIDADE_SAUDE_NOME_FANTA,
    dmundes.dmun_municipio AS UNIDADE_SAUDE_MUNICIPIO,
    dmundes.dmun_regiao AS UNIDADE_SAUDE_REGIAO,
    dmundes.dmun_macro_regiao AS UNIDADE_SAUDE_MACRORREGIAO,
    dmundes.dmun_uf_nomex AS UNIDADE_SAUDE_ESTADO,    
    NU_VPA_TOT VAL_TOT
FROM datalake.refined.sia.pa
INNER JOIN "MariaDB Prod".dimensao.d_municipio dmun
    ON dmun.dmun_codibge = pa.PA_MUNPCN
INNER JOIN "MariaDB Prod".dimensao.d_sigtap sigtap
    ON sigtap.dsig_ipcod = pa.PA_PROC_ID
INNER JOIN "MariaDB Prod".dimensao.d_cid10 cid
     ON cid.dcid_cid10_codigo = PA_CIDPRI
INNER JOIN "MariaDB Prod".dimensao.d_estabelecimento_saude des
    ON des.desa_cnes = PA_CODUNI
INNER JOIN "MariaDB Prod".dimensao.d_municipio dmundes
    ON dmundes.dmun_codibge = des.desa_ibge    
where PA_CMP between 202201 and 202512
limit 500000
"""

# ----------------------------
# FUNÇÃO PARA CONSULTAR DREMIO
# ----------------------------
def get_dremio(sql):

    CONFIG = DREMIO_CONFIG

    conexao = pyodbc.connect(
        "Driver={};"
        "ConnectionType=Direct;"
        "HOST={};"
        "PORT={};"
        "AuthenticationType=Plain;"
        "UID={};"
        "PWD={}".format(
            CONFIG['DRIVER'],
            CONFIG['HOST'],
            CONFIG['PORT'],
            CONFIG['USER'],
            CONFIG['PASSWORD']
        ),
        autocommit=True,
    )

    cursor = conexao.cursor()
    cursor.execute(sql)

    columns = [col[0] for col in cursor.description]
    rows = cursor.fetchall()

    df = pd.DataFrame.from_records(rows, columns=columns)

    conexao.close()

    return df


# ----------------------------
# EXECUTAR CONSULTAS E SALVAR CSVs
# ----------------------------

# INTERNAÇÕES
print("\n" + "="*50)
print("PROCESSANDO INTERNAÇÕES")
print("="*50)
print("Consultando Dremio...")
df_internacoes = get_dremio(SQL_INTERNACOES)

print("Total de registros:", len(df_internacoes))

CSV_PATH_INTERNACOES = "../internacoes.csv"

print("Salvando CSV...")

df_internacoes.to_csv(
    CSV_PATH_INTERNACOES,
    index=False,
    encoding="utf-8"
)

print(f"Arquivo '{CSV_PATH_INTERNACOES}' gerado com sucesso!")

# AMBULATORIAL
print("\n" + "="*50)
print("PROCESSANDO AMBULATORIAL")
print("="*50)
print("Consultando Dremio...")
df_ambulatorial = get_dremio(SQL_AMBULATORIAL)

print("Total de registros:", len(df_ambulatorial))

CSV_PATH_AMBULATORIAL = "../ambulatorial.csv"

print("Salvando CSV...")

df_ambulatorial.to_csv(
    CSV_PATH_AMBULATORIAL,
    index=False,
    encoding="utf-8"
)

print(f"Arquivo '{CSV_PATH_AMBULATORIAL}' gerado com sucesso!")

print("\n" + "="*50)
print("PROCESSAMENTO CONCLUÍDO!")
print("="*50)