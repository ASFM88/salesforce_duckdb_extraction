import duckdb
import sqlite3
import os
import pandas as pd

DUCKDB_PATH = "db/dados_salesforce.duckdb"
SQLITE_PATH = "db/dados_salesforce.db"

def inspecionar_duckdb():
    print(f"\n🦆 DuckDB - {DUCKDB_PATH}")
    if not os.path.exists(DUCKDB_PATH):
        print("❌ Banco DuckDB não encontrado.")
        return
    conn = duckdb.connect(DUCKDB_PATH)
    tabelas = conn.execute("SHOW TABLES").fetchall()
    for t in tabelas:
        nome = t[0]
        print(f"\n📋 Tabela: {nome}")
        print("Campos:")
        print(conn.execute(f'DESCRIBE "{nome}"').fetchdf())
        print("Amostra de dados:")
        print(conn.execute(f'SELECT * FROM "{nome}" LIMIT 5').fetchdf())
    conn.close()

def inspecionar_sqlite():
    print(f"\n💾 SQLite - {SQLITE_PATH}")
    if not os.path.exists(SQLITE_PATH):
        print("❌ Banco SQLite não encontrado.")
        return
    conn = sqlite3.connect(SQLITE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tabelas = cursor.fetchall()
    for t in tabelas:
        nome = t[0]
        print(f"\n📋 Tabela: {nome}")
        estrutura = pd.read_sql_query(f"PRAGMA table_info('{nome}')", conn)
        print("Campos:")
        print(estrutura)
        amostra = pd.read_sql_query(f"SELECT * FROM '{nome}' LIMIT 5", conn)
        print("Amostra de dados:")
        print(amostra)
    conn.close()

if __name__ == "__main__":
    inspecionar_duckdb()
    inspecionar_sqlite()