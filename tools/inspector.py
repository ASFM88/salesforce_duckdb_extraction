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


def inspecionar_banco(nome: str, caminho: str):
    print(f"\n📁 {nome.upper()} - {caminho}")
    if not os.path.exists(caminho):
        print("❌ Banco não encontrado.")
        return

    con = duckdb.connect(caminho)
    tabelas = con.execute("SHOW TABLES").fetchall()

    if not tabelas:
        print("⚠️ Nenhuma tabela encontrada.")
        return

    for (tabela,) in tabelas:
        try:
            df = con.execute(f'SELECT * FROM "{tabela}" LIMIT 5').fetchdf()
            total = con.execute(f'SELECT COUNT(*) FROM "{tabela}"').fetchone()[0]
            print(f"🟢 {tabela} — {df.shape[1]} colunas | {total} linhas")
        except Exception as e:
            print(f"🔴 Erro ao ler '{tabela}': {e}")

    con.close()


if __name__ == "__main__":
    for camada, path in BANCOS_DUCKDB.items():
        inspecionar_banco(camada, path)