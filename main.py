# %%
import duckdb
import pandas as pd
import os

# Cria pasta de saída se não existir
os.makedirs("db", exist_ok=True)

# Conexões com os bancos RAW e STAGE
conn_raw = duckdb.connect("db/raw_salesforce.duckdb")
conn_stage = duckdb.connect("db/stage_salesforce.duckdb")

# Lista de tabelas RAW para processar
objetos_raw = {
    "raw_account": "stage_account",
    "raw_contact": "stage_contact",
    "raw_order": "stage_order"
}

# Loop de transformação básica
for tabela_raw, tabela_stage in objetos_raw.items():
    try:
        df = conn_raw.execute(f'SELECT * FROM "{tabela_raw}"').fetchdf()

        # Exemplo de transformação mínima (expandido depois na camada trusted)
        df = df.fillna("")  # ou ajustes de tipo, normalizações, etc

        # Salva na camada STAGE
        conn_stage.execute(f'DROP TABLE IF EXISTS "{tabela_stage}"')
        conn_stage.execute(f'CREATE TABLE "{tabela_stage}" AS SELECT * FROM df')

        print(f"✅ {tabela_stage}: {len(df)} registros transformados e salvos.")
    except Exception as e:
        print(f"❌ Erro ao processar {tabela_raw} → {e}")

# Fecha conexões
conn_raw.close()
conn_stage.close()

print("✅ Transformação para camada STAGE concluída.")
# %%
