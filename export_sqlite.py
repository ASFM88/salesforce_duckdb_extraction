import os
import duckdb
import sqlite3

EXPORTACOES = [
    ("db/raw_salesforce.duckdb", "db/raw_salesforce.sqlite"),
    ("db/stage_salesforce.duckdb", "db/stage_salesforce.sqlite"),
    ("db/trusted_salesforce.duckdb", "db/trusted_salesforce.sqlite")
]

for caminho_duck, caminho_sqlite in EXPORTACOES:
    camada = caminho_duck.split("/")[-1].replace(".duckdb", "").upper()

    print(f"\n🟠 Exportando camada {camada} para SQLite...")

    con_duck = duckdb.connect(caminho_duck)

    if os.path.exists(caminho_sqlite):
        os.remove(caminho_sqlite)

    con_sqlite = sqlite3.connect(caminho_sqlite)

    tabelas = [row[0] for row in con_duck.execute("SHOW TABLES").fetchall()]

    for tabela in tabelas:
        try:
            df = con_duck.execute(f'SELECT * FROM "{tabela}"').df()
            df.to_sql(tabela, con_sqlite, index=False)
            print(f"✅ Tabela '{tabela}' da camada {camada} salva no SQLite.")
        except Exception as e:
            print(f"❌ Erro ao salvar '{tabela}' da camada {camada}: {e}")

    con_duck.close()
    con_sqlite.close()