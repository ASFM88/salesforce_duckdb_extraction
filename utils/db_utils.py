# db_utils.py
import duckdb # type: ignore
import sqlite3
import pandas as pd
import os

def salvar_em_duckdb(df: pd.DataFrame, tabela: str, caminho: str = "db/dados_salesforce.duckdb"):
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    conn = duckdb.connect(caminho)
    conn.execute(f'DROP TABLE IF EXISTS "{tabela}"')
    conn.execute(f'CREATE TABLE "{tabela}" AS SELECT * FROM df')
    conn.close()

def salvar_em_sqlite(df: pd.DataFrame, tabela: str, caminho: str = "db/dados_salesforce.db"):
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    conn = sqlite3.connect(caminho)
    df.to_sql(tabela, conn, if_exists="replace", index=False)
    conn.close()
