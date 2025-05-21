import duckdb
import os
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Lista de bancos DuckDB por camada
BANCOS_DUCKDB = {
    "RAW": ROOT / "db/raw_salesforce.duckdb",
    "STAGE": ROOT / "db/stage_salesforce.duckdb",
    "TRUSTED": ROOT / "db/trusted_salesforce.duckdb"
}


def inspecionar_duckdb(nome_camada, caminho):
    caminho = str(caminho)
    print(f"\n🦆 DuckDB ({nome_camada}) - {caminho}")
    if not os.path.exists(caminho):
        print("❌ Banco não encontrado.")
        return

    conn = duckdb.connect(caminho)
    tabelas = conn.execute("SHOW TABLES").fetchall()

    if not tabelas:
        print("⚠️ Nenhuma tabela encontrada.")
        conn.close()
        return

    for t in tabelas:
        nome = t[0]
        print(f"\n📋 Tabela: {nome}")
        print("- Campos:")
        print(conn.execute(f'DESCRIBE "{nome}"').fetchdf())
        print("- Amostra de dados:")
        print(conn.execute(f'SELECT * FROM "{nome}" LIMIT 5').fetchdf())

    conn.close()

if __name__ == "__main__":
    for camada, caminho in BANCOS_DUCKDB.items():
        inspecionar_duckdb(camada, caminho)
